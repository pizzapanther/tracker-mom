import pytest

from tmom.exchange.models import FollowRequest, Follow

import nacl.utils
from nacl.public import PrivateKey, Box
from nacl.encoding import URLSafeBase64Encoder

BASE_URL = "/api/v1/exchange"


@pytest.mark.django_db
def test_invite_flow(api_client, django_user_model):
  user1 = django_user_model.objects.create_user(
    username="user1@aol.com", email="user1@aol.com", password="narf"
  )
  api_client.force_login(user1)

  response = api_client.json_post(f"{BASE_URL}/follow/request", {"pubkey": "mypubkey"})
  assert response.status_code == 200
  data = response.json()
  token = data["url"].split("/")[-1]
  assert token

  user2 = django_user_model.objects.create_user(
    username="user2@aol.com", email="user2@aol.com", password="narf"
  )
  api_client.force_login(user2)

  idata = {
    "token": token,
    "pubkey": "mypubkey-user2",
  }
  response = api_client.json_post(f"{BASE_URL}/follow/accept", idata)
  assert response.status_code == 200
  data = response.json()
  assert data["pubkey"]

  req = FollowRequest.objects.get(owner=user1)
  assert req.used_on
  assert req.used_by == user2

  response = api_client.get(f"{BASE_URL}/follow/list")
  data = response.json()
  assert data["count"] == 1
  assert data["items"][0]["email"] == "user1@aol.com"

  api_client.force_login(user1)
  response = api_client.get(f"{BASE_URL}/follow/list")
  data = response.json()
  assert data["count"] == 1
  assert data["items"][0]["email"] == "user2@aol.com"


@pytest.mark.django_db
def test_send_messages(api_client, django_user_model):
  user1 = django_user_model.objects.create_user(
    username="user1@aol.com", email="user1@aol.com", password="narf"
  )
  user2 = django_user_model.objects.create_user(
    username="user2@aol.com", email="user2@aol.com", password="narf"
  )

  pkey1 = PrivateKey.generate()
  pubkey1 = pkey1.public_key.encode(encoder=URLSafeBase64Encoder).decode()
  pkey2 = PrivateKey.generate()
  pubkey2 = pkey2.public_key.encode(encoder=URLSafeBase64Encoder).decode()

  f1 = Follow(owner=user1, following=user2, follow_pubkey=pubkey2)
  f1.save()

  f2 = Follow(owner=user2, following=user1, follow_pubkey=pubkey1)
  f2.save()

  box1 = Box(pkey1, pkey2.public_key)
  etext1 = box1.encrypt(b'narf', encoder=URLSafeBase64Encoder).decode()

  box2 = Box(pkey2, pkey1.public_key)
  etext2 = box2.encrypt(b'barf', encoder=URLSafeBase64Encoder).decode()

  api_client.force_login(user1)
  data = [{
    "follow_id": f1.id,
    "payload": etext1,
  }]
  response = api_client.json_post(f"{BASE_URL}/location/push", data)
  assert response.status_code == 200

  api_client.force_login(user2)
  data = [{
    "follow_id": f2.id,
    "payload": etext2,
  }]
  response = api_client.json_post(f"{BASE_URL}/location/push", data)
  assert response.status_code == 200

  api_client.force_login(user1)
  response = api_client.get(f"{BASE_URL}/location/list")
  data = response.json()

  print(data)

  api_client.force_login(user2)
  response = api_client.get(f"{BASE_URL}/location/list")
  data = response.json()

  print(data)
