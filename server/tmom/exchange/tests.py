import pytest


@pytest.mark.django_db
def test_api_invite(api_client, django_user_model):
  user = django_user_model.objects.create_user(username='user1@aol.com', password='narf')
  api_client.force_login(user)
  response = api_client.json_post('/api/v1/exchange/follow/request', {'pubkey': 'mypubkey'})
  assert response.status_code == 200
  data = response.json()
  token = data['url'].split("/")[-1]
  print(token)
