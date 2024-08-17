from fastapi import APIRouter, Response, Depends, HTTPException, BackgroundTasks
from users.scheme import SchemeUserAuth
from users.dao import UserDAO
from users.auth import get_password_hash, authenticate_user, create_access_token
from users.model import User
from users.dependencies import get_current_user
from exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from database import async_session_maker
from bookings.dao import BookingDAO
from bookings.scheme import SchemeBooking
from tasks.tasks import registration_message
from config import settings
from fastapi.responses import RedirectResponse
import jwt
from jose import JWTError

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
async def register_user(user_data: SchemeUserAuth,
                        background_tasks: BackgroundTasks):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)

    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)

    background_tasks.add_task(registration_message, user_data.email)


@router.get("/verify-email")
async def verify_email(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        user = await UserDAO.find_one_or_none(email=email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_email_verified = True
        await UserDAO.update(user)
        return RedirectResponse(url=f"{settings.FRONTEND_URL}")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token or token has expired")


@router.post("/login")
async def login_user(response: Response, user_data: SchemeUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException

    if not user.is_email_verified:
        raise HTTPException(status_code=403, detail="Пожалуйста, подтвердите вашу электронную почту перед входом")
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/me")
async def read_user_me(current_user: User = Depends(get_current_user)):
    async with async_session_maker() as session:
        bookings = await BookingDAO.get_bookings_by_user_id(current_user.id)
        if not bookings:
            return {
                "user": current_user,
                "bookings": [],
                "message": "у вас пока нет бронирований"
            }
        bookings_schema = [SchemeBooking.from_orm(booking) for booking in bookings]
    return {
        "user": current_user,
        "bookings": bookings_schema
    }
