from django.contrib import admin
from .models import Visitor, VisitLog


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "visit_count", "first_seen",
                    "last_seen", "country", "city")
    search_fields = ("ip_address", "country", "city", "isp")
    readonly_fields = ("first_seen", "last_seen")
    list_filter = ("country",)
    ordering = ("-last_seen",)
    list_per_page = 25


@admin.register(VisitLog)
class VisitLogAdmin(admin.ModelAdmin):
    list_display = ("visitor", "path", "method", "timestamp")
    search_fields = ("visitor__ip_address", "path")
    list_filter = ("method",)
    date_hierarchy = "timestamp"
    readonly_fields = ("visitor", "path", "method", "timestamp", "meta")
