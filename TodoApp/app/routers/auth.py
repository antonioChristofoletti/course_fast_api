from datetime import datetime, timezone, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, Path, Request, status, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
import bcrypt
from fastapi.templating import Jinja2Templates

from app.config.models import Users
from app.config.database import db_dependency


router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "92b3e8c838b9c70524d8aa486af8011ebd330865465e905d9a66417f2f27bdd9222b3ef342b6e143c5dd850fee079132faac679c49b6ba7ab055424b0626234e"
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str


class EditPhoneNumberUserRequest(BaseModel):
    phone_number: str


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False

    if not bcrypt.checkpw(
        password.encode("utf-8"), user.hashed_password.encode("utf-8")
    ):
        return False

    return user


def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
):

    encode = {"sub": username, "id": user_id, "role": role}

    expires = datetime.now(timezone.utc) + expires_delta

    encode.update({"exp": expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        user_role: str = payload.get("role")

        if username is None or user_id is None or user_role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )

        return {"username": username, "id": user_id, "role": user_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )


user_dependency = Annotated[dict, Depends(get_current_user)]

templates = Jinja2Templates(directory="templates")

### Pages ###


@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


### Endpoints ###
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, create_user_request: CreateUserRequest):

    user_dict = create_user_request.model_dump()

    password = user_dict["password"]
    del user_dict["password"]
    bytes = password.encode("utf-8")
    hash = bcrypt.hashpw(bytes, bcrypt.gensalt()).decode("utf-8")
    user_dict["hashed_password"] = hash

    user_dict["is_active"] = True

    user = Users(**user_dict)

    db.add(user)
    db.commit()


@router.patch("/phonenumber/{user_id}", status_code=status.HTTP_200_OK)
def edit_user(
    user: user_dependency,
    db: db_dependency,
    edit_user_request: EditPhoneNumberUserRequest,
    user_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_id_token: int = user.get("id")

    if user_id != user_id_token:
        raise HTTPException(
            status_code=401,
            detail=f"The user id '{user_id}' should be the same as the user_id in the token '{user_id_token}'",
        )

    user: Users | None = db.query(Users).filter(Users.id == user_id).first()

    if user is None:
        raise HTTPException(f"The user_id '{user_id}' informed was not found")

    user.phone_number = edit_user_request.phone_number

    db.add(user)

    db.commit()


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):

    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )

    token = create_access_token(
        user.username, user.id, user.role, timedelta(minutes=20)
    )

    return {"access_token": token, "token_type": "bearer"}
