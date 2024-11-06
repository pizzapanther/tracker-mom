from ninja import NinjaAPI, Redoc
from ninja.security import django_auth

from tmom.exchange.api import router as exchange_router

api_v1 = NinjaAPI(docs=Redoc(), auth=django_auth)

api_v1.add_router("/exchange/", exchange_router, tags=["exchange"])
