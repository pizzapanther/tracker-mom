import datetime
import random
from typing import List

import jwt
from ninja import Router
from ninja.errors import HttpError
from ninja.pagination import paginate
from wonderwords import RandomWord

from django.conf import settings
from django.utils import timezone

from tmom.exchange.models import FollowRequest, Follow, LocationShare
from tmom.exchange.schema import (
  InviteSchema,
  FollowInput,
  FollowSchema,
  AcceptInput,
  AuthSchema,
  LocationShareInput,
  SavedStatusSchema,
  LocationShareSchema,
)

router = Router()


@router.post("/follow/request", response=InviteSchema)
def request_location_share(request, data: FollowInput):
  rw = RandomWord()
  while 1:
    word = rw.word(word_min_length=4, word_max_length=5)
    num = str(random.randint(0, 9999))
    num = num.zfill(4)
    code = f"{word}-{num}"

    if FollowRequest.objects.filter(code=code).count() == 0:
      break

  req = FollowRequest(owner=request.user, code=code, pubkey=data.pubkey)
  req.save()

  payload = {
    "invite-code": code,
    "exp": timezone.now() + datetime.timedelta(minutes=settings.FOLLOW_REQUEST_EXPIRATION),
  }
  encoded = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
  return {"status": "OK", "url": f"{settings.APP_BASE_URL}/account/accept-invite/{encoded}"}


@router.post("/follow/accept", response=FollowSchema)
def accept_location_share(request, data: AcceptInput):
  try:
    payload = jwt.decode(data.token, settings.SECRET_KEY, algorithms=["HS256"])

  # ruff: noqa: E722
  except:
    return HttpError(400, "Invalid token")

  req = FollowRequest.objects.filter(code=payload["invite-code"]).first()
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
  session = getattr(request, 'api_session', request.session)
  return {"id": request.user.id, "expires": session.get_expiry_date().isoformat()}


@router.get("/follow/list", response=List[FollowSchema])
@paginate
def follow_list(request):
  return Follow.objects.filter(owner=request.user).order_by("-created")


@router.post("/location/push", response=SavedStatusSchema)
def location_push(request, data: List[LocationShareInput]):
  cnt = 0
  for d in data:
    follow = Follow.objects.filter(owner=request.user, following=d.following, active=True).first()

    if follow:
      share = LocationShare(follow=follow, payload=d.payload)
      share.save()
      cnt += 1

  return {"status": "OK", "saved": cnt}


@router.get("/location/list", response=List[LocationShareSchema])
@paginate
def location_list(request):
  qs = LocationShare.objects.filter(follow__following=request.user)
  LocationShare.cleanup(qs)
  return qs
