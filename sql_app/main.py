from datetime import timedelta
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import crud, models, schemas, security
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = security.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(
    skip: int = 0, limit: int = 100,
    current_user: schemas.User = Depends(security.get_current_active_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an administrator")
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    current_user: schemas.User = Depends(security.get_current_active_user),
    db: Session = Depends(get_db)
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if db_user != current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You do not have permission to access")
    return db_user

@app.post("/users/{user_id}/items", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate,
    current_user: schemas.User = Depends(security.get_current_active_user),
    db: Session = Depends(get_db)
):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You do not have permission to access")
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@app.get("/items", response_model=List[schemas.Item])
def read_items(
    skip: int = 0, limit: int = 100,
    current_user: schemas.User = Depends(security.get_current_active_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an administrator")
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


