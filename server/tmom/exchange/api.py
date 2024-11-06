import random

from ninja import Router, Schema
from wonderwords import RandomWord

from tmom.exchange.models import FollowRequest

router = Router()


class MessageSchema(Schema):
  message: str
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

  req = FollowRequest()
  req.save()

  return {'message': 'narf', 'url': 'url-out'}
