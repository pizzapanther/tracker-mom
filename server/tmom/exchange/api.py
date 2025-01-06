import datetime
from typing import List

from haikunator import Haikunator

from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import paginate

from django.conf import settings
from django.utils import timezone

from tmom.exchange.models import FollowRequest, Follow, LocationShare
from tmom.exchange.schema import (
  InviteSchema,
  FollowInput,
  FollowSchema,
  RequestSchema,
  AcceptInput,
  AuthSchema,
  LocationShareInput,
  SavedStatusSchema,
  LocationShareSchema,
)

router = Router()


@router.post("/follow/request", response=InviteSchema)
def request_location_share(request, data: FollowInput):
  """
  Create a location share request
  """
  haikunator = Haikunator()
  while 1:
    code = haikunator.haikunate()
    if FollowRequest.objects.filter(code=code).count() == 0:
      break

  req = FollowRequest(owner=request.user, code=code, pubkey=data.pubkey)
  req.save()

  return {"status": "OK", "url": f"{settings.APP_BASE_URL}/#/invite/{code}"}


@router.get("/follow/accept", response=RequestSchema)
def view_location_share(request, code: str):
  """
  Get share request
  """
  old = timezone.now() - datetime.timedelta(minutes=settings.FOLLOW_REQUEST_EXPIRATION)
  req = FollowRequest.objects.filter(code=code, created__gte=old, used_on__isnull=True).first()
  if req is None:
    return HttpError(400, "Invalid invite code")

  return req


@router.post("/follow/accept", response=FollowSchema)
def accept_location_share(request, data: AcceptInput):
  """
  Accept share request
  """
  old = timezone.now() - datetime.timedelta(minutes=settings.FOLLOW_REQUEST_EXPIRATION)
  req = FollowRequest.objects.filter(code=data.code, created__gte=old, used_on__isnull=True).first()
  if req is None:
    return HttpError(400, "Invalid invite code")

  now = timezone.now()
  Follow.objects.filter(owner=req.owner, following=request.user).update(
    active=False, active_off_on=now
  )
  Follow.objects.filter(owner=request.user, following=req.owner).update(
    active=False, active_off_on=now
  )

  f1 = Follow(owner=req.owner, following=request.user, follow_pubkey=data.pubkey)
  f2 = Follow(owner=request.user, following=req.owner, follow_pubkey=req.pubkey)
  f1.save()
  f2.save()

  req.used_by = request.user
  req.used_on = now
  req.save()

  return f2


@router.get("/auth/check", response=AuthSchema)
def auth_check(request):
  """
  Get user session expiration timestamp
  """
  session = getattr(request, 'api_session', request.session)
  return {
    "id": request.user.id,
    "expires": session.get_expiry_date().isoformat(),
    "email": request.user.email,
  }


@router.get("/follow/list", response=List[FollowSchema])
@paginate
def follow_list(request):
  """
  List user follows
  """
  if request.method == "OPTIONS":
    return Follow.objects.none()

  return Follow.objects.filter(owner=request.user, active=True).order_by("-created")


@router.post("/location/push", response=SavedStatusSchema)
def location_push(request, data: LocationShareInput):
  """
  Push location messages to followers
  """
  cnt = 0
  for d in data.messages:
    follow = Follow.objects.filter(owner=request.user, following=d.following, active=True).first()

    if follow:
      if data.clear_previous:
        LocationShare.objects.filter(follow=follow).delete()

      share = LocationShare(follow=follow, payload=d.payload)
      share.save()
      cnt += 1

  return {"status": "OK", "saved": cnt}


@router.get("/location/list", response=List[LocationShareSchema])
@paginate
def location_list(request):
  """
  Pull user location messages
  """

  if request.method == "OPTIONS":
    return LocationShare.objects.none()

  qs = LocationShare.objects.filter(follow__following=request.user)
  LocationShare.cleanup(qs)
  return qs.order_by("-created")
