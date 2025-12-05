from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.utils import timezone
from .models import Visitor, VisitLog
from datetime import timedelta


@staff_member_required
def dashboard(request):
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    last_24h = now - timedelta(hours=24)

    recent_visitors = Visitor.objects.all()[:10]
    unique_today = Visitor.objects.filter(last_seen__gte=today_start).count()
    total_unique = Visitor.objects.count()
    visits_24h = VisitLog.objects.filter(timestamp__gte=last_24h)
    total_visits_24h = visits_24h.count()

    # Most visited paths - top 10
    top_paths = (
        VisitLog.objects.values("path")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    context = {
        "recent_visitors": recent_visitors,
        "unique_today": unique_today,
        "total_unique": total_unique,
        "total_visits_24h": total_visits_24h,
        "top_paths": top_paths,
    }
    return render(request, "iplogger/dashboard.html", context)
