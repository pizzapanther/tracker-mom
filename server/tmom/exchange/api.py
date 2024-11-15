import datetime
import random
from typing import List

import jwt
from ninja import Router, Schema, ModelSchema
from ninja.errors import HttpError
from ninja.pagination import paginate
from wonderwords import RandomWord

from django.conf import settings
from django.utils import timezone

from tmom.exchange.models import FollowRequest, Follow

router = Router()


class InviteSchema(Schema):
  status: str
  url: str


class FollowInput(Schema):
  pubkey: str


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
    "exp": timezone.now() + datetime.timedelta(days=3),
  }
  encoded = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
  return {"status": "OK", "url": f"{settings.APP_BASE_URL}/account/accept-invite/{encoded}"}


class FollowSchema(ModelSchema):
  email: str
  pubkey: str
  name: str

  class Meta:
    model = Follow
    fields = ["id"]


class AcceptInput(Schema):
  token: str
  pubkey: str


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

  f1 = Follow(owner=req.owner, following=request.user, follow_pubkey=data.pubkey)
  f2 = Follow(owner=request.user, following=req.owner, follow_pubkey=req.pubkey)
  f1.save()
  f2.save()

  req.used_by = request.user
  req.used_on = timezone.now()
  req.save()

  return f2


class AuthSchema(Schema):
  id: int
  expires: str


@router.get("/auth/check", response=AuthSchema)
def auth_check(request):
  return {"id": request.user.id, "expires": request.session.get_expiry_date().isoformat()}


@router.get("/follow/list", response=List[FollowSchema])
@paginate
def follow_list(request):
  return Follow.objects.filter(owner=request.user).order_by("-created")
