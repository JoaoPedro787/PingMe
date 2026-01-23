from fastapi import FastAPI, Depends
from database import create_db_and_tables
from auth.dependencies import validate_user_token
from auth.router import router as auth_router
from chat.router import router as chat_router
from ws.router import router as ws_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def index():
    return {"hello": "Hello, worldl!"}


app.include_router(router=auth_router, prefix="/auth", tags=["auth"])

app.include_router(
    router=chat_router,
    prefix="/chat",
    tags=["chat"],
    dependencies=[Depends(validate_user_token)],
)

app.include_router(router=ws_router, prefix="/ws", tags=["websockets"])
