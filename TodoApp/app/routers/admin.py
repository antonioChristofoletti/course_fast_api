from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi import HTTPException, Path, status

from app.config.models import Todos
from app.routers.auth import get_current_user
from app.config.database import db_dependency

router = APIRouter(prefix="/admin", tags=["admin"])

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
def read_all(user: user_dependency, db: db_dependency):

    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")

    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
