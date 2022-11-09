from email.policy import default
from turtle import mode
from unittest.mock import DEFAULT
from django.db import models
from django.contrib.auth.models import User


class SearchTerm(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class SearchResult(models.Model):
    CLAIMED = "claimed"   # Username Detected
    AVAILABLE = "available"  # Username Not Detected
    UNKNOWN = "unknown"   # Error Occurred While Trying To Detect Username
    ILLEGAL = "illegal"   # This format of Username Not Allowable For This Site

    SEARCH_CHOICES = (
        (CLAIMED,   "Claimed"),
        (AVAILABLE, "Available"),
        (UNKNOWN,   "Unknown"),
        (ILLEGAL,   "Illegal"),
    )
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    term = models.ForeignKey(SearchTerm, on_delete=models.CASCADE)
    sitename = models.CharField(max_length=50)
    url = models.URLField(max_length=200)
    search_status = models.CharField(
        max_length=20, choices=SEARCH_CHOICES, default=AVAILABLE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.term
