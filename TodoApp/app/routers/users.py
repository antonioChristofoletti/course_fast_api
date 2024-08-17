import bcrypt
from fastapi import APIRouter, status, HTTPException, Path, Query
from pydantic import BaseModel, Field
from app.config.models import Users
from app.routers.auth import authenticate_user, user_dependency
from app.config.database import Base, db_dependency


router = APIRouter(prefix="/user", tags=["user"])


class UsersChangePasswordRequest(BaseModel):
    password: str
    new_password: str = Field(min_length="4")


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user: user_dependency, db: db_dependency, user_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_id_token: int = user.get("id")

    if user_id != user_id_token:
        raise HTTPException(
            status_code=401,
            detail=f"The user id '{user_id}' should be the same as the user_id in the token '{user_id_token}'",
        )

    return db.query(Users).filter(Users.id == user.get("id")).first()


@router.put("/password/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def update(
    user: user_dependency,
    db: db_dependency,
    pass_req: UsersChangePasswordRequest,
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

    if not bcrypt.checkpw(pass_req.password.encode("utf-8"), user.hashed_password.encode("utf-8")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The password informed does not match with the current password",
        )

    if user is None:
        raise HTTPException(f"The user_id '{user_id}' informed was not found")

    user.hashed_password = bcrypt.hashpw(
        pass_req.new_password.encode("utf-8"), bcrypt.gensalt()
    )

    db.add(user)
    db.commit()
