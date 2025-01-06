from typing import List

from django.contrib.auth import get_user_model

from ninja import Schema, ModelSchema
from pydantic import computed_field

from tmom.exchange.models import Follow, FollowRequest, LocationShare

User = get_user_model()


class AuthSchema(Schema):
  id: int
  expires: str
  email: str


class UserSchema(ModelSchema):
  @computed_field
  @property
  def name(self) -> str:
    full_name = "%s %s" % (self.first_name, self.last_name)
    full_name = full_name.strip()
    return full_name or self.email

  class Meta:
    model = User
    fields = ["id", "email", "first_name", "last_name"]


class OwnerSchema(ModelSchema):
  @computed_field
  @property
  def name(self) -> str:
    full_name = "%s %s" % (self.first_name, self.last_name)
    full_name = full_name.strip()
    return full_name or self.email

  class Meta:
    model = User
    fields = ["email", "first_name", "last_name"]


class InviteSchema(Schema):
  status: str
  url: str


class FollowInput(Schema):
  pubkey: str


class RequestSchema(ModelSchema):
  owner: OwnerSchema

  class Meta:
    model = FollowRequest
    fields = ["created"]


class FollowSchema(ModelSchema):
  following: UserSchema
  owner_pubkey: str

  class Meta:
    model = Follow
    fields = ["follow_pubkey", "created"]


class AcceptInput(Schema):
  code: str
  pubkey: str


class MessageInput(Schema):
  following: int
  payload: str


class LocationShareInput(Schema):
  clear_previous: bool
  messages: List[MessageInput]


class SavedStatusSchema(Schema):
  status: str
  saved: int


class LocationShareSchema(ModelSchema):
  posted_by: UserSchema

  class Meta:
    model = LocationShare
    fields = ["id", "payload", "created"]


