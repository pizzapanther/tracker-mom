import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.functions import Now
from django.utils import timezone

from allauth.account.models import EmailAddress
from simple_history import register
from simple_history.models import HistoricalRecords

register(User)
register(EmailAddress)


class Follow(models.Model):
  owner = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="follows"
  )
  following = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers"
  )

  follow_pubkey = models.TextField()

  active = models.BooleanField(default=True)

  created = models.DateTimeField(db_default=Now())

  history = HistoricalRecords()

  class Meta:
    ordering = ["-created"]

  def __str__(self):
    return f"{self.owner} -> {self.following}"

  @property
  def name(self):
    return self.following.get_full_name() or self.following.email

  @property
  def email(self):
    return self.following.email

  @property
  def pubkey(self):
    return self.follow_pubkey


class FollowRequest(models.Model):
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  code = models.CharField(max_length=15)

  pubkey = models.TextField()

  used_on = models.DateTimeField(blank=True, null=True)
  used_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="accepted_requests",
    blank=True,
    null=True,
  )

  created = models.DateTimeField(db_default=Now())

  history = HistoricalRecords()

  class Meta:
    ordering = ["-created"]

  def __str__(self):
    return f"{self.owner}"


class LocationShare(models.Model):
  follow = models.ForeignKey(Follow, on_delete=models.CASCADE)
  payload = models.TextField()

  created = models.DateTimeField(db_default=Now())

  class Meta:
    ordering = ["created"]

  def __str__(self):
    return f"{self.follow}"

  @classmethod
  def cleanup(cls):
    old = timezone.now() - datetime.timedelta(minutes=settings.EXCHANGE_EXPIRATION)
    cls.filter(created__lte=old).delete()
