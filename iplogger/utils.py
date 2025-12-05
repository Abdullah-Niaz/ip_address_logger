import requests
from django.conf import settings


def get_client_ip(request):
    """
    Robust IP extraction. Prefer X-Forwarded-For if behind proxy.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # X-Forwarded-For may contain a comma separated list. Client IP is first.
        ip = x_forwarded_for.split(",")[0].strip()
        if ip:
            return ip
    # Fallbacks
    ip = request.META.get("REMOTE_ADDR")
    return ip


def lookup_ip_geo(ip: str):
    """
    Simple optional IP -> geo lookup using ipapi.co (no key required for basic usage).
    Returns a dict with keys or None on failure.
    To use a different service, change the implementation. Raise no exceptions.
    """
    if not ip:
        return None

    try:
        # Example using ipapi.co. For production, respect rate limits and use API key if required.
        url = f"https://ipapi.co/{ip}/json/"
        resp = requests.get(url, timeout=4)
        if resp.status_code != 200:
            return None
        data = resp.json()
        return {
            "country": data.get("country_name"),
            "region": data.get("region"),
            "city": data.get("city"),
            "isp": data.get("org"),
        }
    except Exception:
        return None
