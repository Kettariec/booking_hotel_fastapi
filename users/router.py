from fastapi import APIRouter, Response, Depends
from users.scheme import SchemeUserAuth
from users.dao import UserDAO
from users.auth import get_password_hash, authenticate_user, create_access_token
from users.model import User
from users.dependencies import get_current_user
from exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from database import async_session_maker
from bookings.dao import BookingDAO
from bookings.scheme import SchemeBooking

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
async def register_user(user_data: SchemeUserAuth):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SchemeUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
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
