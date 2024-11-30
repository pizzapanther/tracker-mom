from django.conf import settings
from django.contrib.auth import load_backend

from ninja import NinjaAPI, Redoc
from ninja.security.session import SessionAuth

from allauth.headless import app_settings
from allauth.headless.internal.authkit import purge_request_user_cache

from tmom.exchange.api import router as exchange_router

class AllAuthHeadless(SessionAuth):
  def authenticate(self, request, key=None):
    strategy = app_settings.TOKEN_STRATEGY
    session_token = strategy.get_session_token(request)
    if session_token:
      session = strategy.lookup_session(session_token)
      if session:
        user_id = session.get('_auth_user_id', None)
        backend_path = session.get('_auth_user_backend', None)
        if user_id and backend_path in settings.AUTHENTICATION_BACKENDS:
          backend = load_backend(backend_path)
          user = backend.get_user(user_id)

          if user.is_authenticated:
            purge_request_user_cache(request)
            request.user = user
            request.api_session = session
            return user

    if request.user.is_authenticated:
      return request.user

    return None


allauth_headless = AllAuthHeadless()


api_v1 = NinjaAPI(
  title="Tracker Mom API", description="OpenAPI Docs", docs=Redoc(), auth=allauth_headless
)

api_v1.add_router("/exchange/", exchange_router, tags=["exchange"])
