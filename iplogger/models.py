from django.db import models
from django.utils import timezone

class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    isp = models.CharField(max_length=255, blank=True, null=True)
    first_seen = models.DateTimeField(default=timezone.now)
    last_seen = models.DateTimeField(default=timezone.now)
    visit_count = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=["ip_address"]),
            models.Index(fields=["last_seen"]),
        ]
        ordering = ["-last_seen"]

    def __str__(self):
        return f"{self.ip_address} ({self.visit_count})"


class VisitLog(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name="visits")
    path = models.CharField(max_length=500)
    method = models.CharField(max_length=10, blank=True)
    status_code = models.PositiveSmallIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    meta = models.JSONField(blank=True, null=True)  # optional extra info

    class Meta:
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["path"]),
        ]
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.visitor.ip_address} @ {self.timestamp:%Y-%m-%d %H:%M:%S} -> {self.path}"
