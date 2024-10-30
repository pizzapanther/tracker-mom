from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.functions import Now

from allauth.account.models import EmailAddress
from simple_history import register
from simple_history.models import HistoricalRecords

register(User)
register(EmailAddress)


class Follow(models.Model):
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="follows")
  following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers")

  pubkey = models.TextField()

  active = models.BooleanField(default=True)
  approved = models.BooleanField(default=False)

  created = models.DateTimeField(db_default=Now())

  history = HistoricalRecords()

  class Meta:
    ordering = ["-created"]

  def __str__(self):
    return f"{self.owner} -> {self.following}"
