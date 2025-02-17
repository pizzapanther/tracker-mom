import datetime

from django.conf import settings
from django.db import models
from django.db.models.functions import Now
from django.utils import timezone


class Follow(models.Model):
  owner = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="follows"
  )
  following = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers"
  )

  follow_pubkey = models.TextField()

  active = models.BooleanField(default=True)
  active_off_on = models.DateTimeField(blank=True, null=True)

  created = models.DateTimeField(db_default=Now())

  class Meta:
    ordering = ["-created"]

  def __str__(self):
    return f"{self.owner} -> {self.following}"

  @property
  def owner_pubkey(self):
    follow_back = Follow.objects.filter(owner=self.following, following=self.owner).first()
    return follow_back.follow_pubkey


class FollowRequest(models.Model):
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  code = models.CharField(max_length=155)

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
  def cleanup(cls, qs=None):
    old = timezone.now() - datetime.timedelta(minutes=settings.EXCHANGE_EXPIRATION)
    if qs is None:
      qs = cls.objects.all()

    return qs.filter(created__lte=old).delete()

  @property
  def posted_by(self):
    return self.follow.owner
