from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from config import settings
from users.auth import authenticate_user, create_access_token
from exceptions import IncorrectEmailOrPasswordException
from users.dependencies import get_current_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        user = await authenticate_user(email, password)
        if user:
            access_token = create_access_token({"sub": str(user.id)})
            request.session["token"] = access_token
            return True
        else:
            raise IncorrectEmailOrPasswordException

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        try:
            user = await get_current_user(token)
            return True
        except Exception as e:
            return False


authentication_backend = AdminAuth(secret_key="...")
