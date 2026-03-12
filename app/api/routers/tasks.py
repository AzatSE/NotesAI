from typing import Annotated
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
import uuid


from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.schemas import TaskCreate, TaskRead, EditTask, TaskComlite
from app.models import User, Task

router = APIRouter(
    tags=["Tasks"]
)


@router.post("/tasks", response_model=TaskRead)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not task.task.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task cannot be empty"
        )

    new_task = Task(
        user_id=current_user.id,
        task=task.task.strip(),
        comlite=False
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
@router.put("/tasks/{task_id}/completed")
async def comlete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)

    task.comlite = not task.comlite

    db.commit()

    return {"completed": task.comlite}

@router.delete("/tasks/{task_id}")
async def delete_task(task_id:int, db:Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    db.delete(task)
    db.commit()
    return {"complete": task}


@router.get("/users/{user_id}/tasks", response_model=list[TaskRead])
def get_user_posts(user_id: int, db:Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.user_id == user_id).all()

    return tasks








# @router.put("/posts/{post_id}", response_model=PostRead)
# def edit_post(
#         post_id: int,
#         text: EditPost,
#         current_user: Annotated[UserModel, Depends(get_current_user)],
#         db: Session = Depends(get_db)
# ):
#     if not current_user:
#         raise HTTPException(status_code=401, detail="Not Authenticated")
#     edited_post = db.query(PostModel).filter(PostModel.id == post_id).first()
#     if not edited_post:
#         raise HTTPException(status_code=404, detail="Not accepted")
#
#     for key,value in text.dict(exclude_unset=True).items():
#         setattr(edited_post, key, value)
#     db.commit()
#     db.refresh(edited_post)
#
#     return edited_post
#
# @router.get("/posts", response_model=list[PostRead])
# def get_all_posts(db: Session = Depends(get_db)):
#     posts = db.query(PostModel).all()
#
#     return posts
#
#
#
# @router.get("/users/{user_id}/posts", response_model=list[PostRead])
# def get_user_posts(user_id: int, db:Session = Depends(get_db)):
#     posts = db.query(PostModel).filter(PostModel.user_id == user_id).all()
#
#     return posts
#
# @router.delete("/posts/delete/{post_id}/")
# async def delete_post(
#         post_id: int,
#         db: Session = Depends(get_db)
# ):
#     post = db.query(PostModel).filter(PostModel.id == post_id).first()
#     db.delete(post)
#     db.commit()
#     return f"post {post_id} was deleted"
#
# @router.get("/following/posts", response_model=list[PostRead])
# async def get_following_posts(
#         current_user: Annotated[UserModel, Depends(get_current_user)],
#         db: Session = Depends(get_db)
# ):
#     posts = (
#         db.query(PostModel)
#         .join(FollowModel, FollowModel.following_id == PostModel.user_id)
#         .filter(FollowModel.follower_id == current_user.id)
#
#     )
#     return posts
# @router.get("/posts/{post_id}/")
# async def get_one_post(
#         post_id: int,
#         current_user: Annotated[UserModel, Depends(get_current_user)],
#         db: Session = Depends(get_db),
# ):
#     if not current_user:
#         raise HTTPException(
#             status_code=401,
#             detail="Not Authorised"
#         )
#     post = db.query(PostModel).filter(PostModel.id == post_id).first()
#     return post