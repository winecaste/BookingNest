from fastapi import APIRouter, Response, Depends, Request, responses, status, Form
from pydantic import EmailStr

from app.exceptions import UserAlreadyExistException, IncorrectAccessException
from app.pages.router import templates
from app.users.auth import get_password_hash, create_access_token, authenticate_user
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth
from fastapi.responses import RedirectResponse

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)


@router.get("/register")
async def home(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", status_code=201)
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)




@router.get("/login")
def signup(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectAccessException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.post("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user
