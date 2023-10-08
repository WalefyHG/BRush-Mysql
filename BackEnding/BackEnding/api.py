from ninja import NinjaAPI
from BRushAPI.routers.user import router as UserRouter
from BRushAPI.routers.team import router as TeamRouter
from rest_framework_simplejwt.authentication import JWTAuthentication
from ninja.security import HttpBearer

class JWTBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            user = JWTAuthentication().authenticate(request)
        except:
            return None
        if user is None:
            return None
        return user[0]

api = NinjaAPI()

api.add_router("/users", UserRouter, tags=["Users"], auth=JWTBearer())
api.add_router("/teams", TeamRouter, tags=["Team"], auth=JWTBearer())