from django.utils import timezone
from django.conf import settings
from .models import Visitor, VisitLog
from .utils import get_client_ip, lookup_ip_geo


class VisitorTrackingMiddleware:
    """
    Place this middleware early in MIDDLEWARE list so it runs for each request.
    It will create/update Visitor and append a VisitLog.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Optionally disable heavy work like geo lookups in DEBUG or via settings.
        self.enable_geo = getattr(settings, "IPLOGGER_ENABLE_GEO", False)

    def __call__(self, request):
        # We track only for HTTP(S) requests that are not static/media and not admin static files.
        path = request.path or ""
        # Optionally ignore admin or static files
        ignored_prefixes = getattr(settings, "IPLOGGER_IGNORED_PREFIXES", [
                                   "/static/", "/media/"])
        if any(path.startswith(p) for p in ignored_prefixes):
            return self.get_response(request)

        ip = get_client_ip(request)
        ua = request.META.get("HTTP_USER_AGENT", "")[:1000]  # limit length

        # Create or update Visitor
        if ip:
            now = timezone.now()
            visitor, created = Visitor.objects.get_or_create(
                ip_address=ip,
                defaults={
                    "user_agent": ua,
                    "first_seen": now,
                    "last_seen": now,
                    "visit_count": 1,
                },
            )
            if not created:
                visitor.user_agent = ua or visitor.user_agent
                visitor.last_seen = now
                visitor.visit_count = (visitor.visit_count or 0) + 1
                visitor.save(update_fields=[
                             "user_agent", "last_seen", "visit_count"])

            # Optionally enrich with geo info if missing and enabled
            if self.enable_geo and (not visitor.country and not visitor.city):
                geo = lookup_ip_geo(ip)
                if geo:
                    visitor.country = geo.get("country")
                    visitor.region = geo.get("region")
                    visitor.city = geo.get("city")
                    visitor.isp = geo.get("isp")
                    visitor.save(update_fields=[
                                 "country", "region", "city", "isp"])

            # Log the visit
            VisitLog.objects.create(
                visitor=visitor,
                path=path,
                method=request.method,
                # status_code is unknown until response; if you want it, create a second-phase logger.
                meta={
                    "headers": {
                        "referer": request.META.get("HTTP_REFERER"),
                    }
                },
            )

        response = self.get_response(request)
        return response
