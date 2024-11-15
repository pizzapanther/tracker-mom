import pytest

from tmom.exchange.models import FollowRequest

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
