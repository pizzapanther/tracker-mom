import random

import jwt
from ninja import Router, Schema
from wonderwords import RandomWord

from django.conf import settings

from tmom.exchange.models import FollowRequest

router = Router()


class MessageSchema(Schema):
  status: str
  url: str


class FollowInput(Schema):
  pubkey: str


@router.post('/follow/request', response=MessageSchema)
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

  encoded = jwt.encode({"invite-code": code}, settings.SECRET_KEY, algorithm="HS256")
  return {'status': 'OK', 'url': f'{settings.APP_BASE_URL}/account/accept-invite/{encoded}'}
