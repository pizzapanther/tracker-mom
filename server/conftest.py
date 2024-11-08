import json

import pytest


def json_post(client):
  def caller (url, jdata, *args, **kwargs):
    return client.post(url, json.dumps(jdata), *args, content_type="application/json", **kwargs)

  return caller


@pytest.fixture
def api_client(client):
  client.json_post = json_post(client)
  return client
