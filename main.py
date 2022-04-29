import uvicorn
from fastapi import FastAPI #, HTTPException, Depends, Request, BackgroundTasks, Response, status, File, UploadFile
# from fastapi.responses import JSONResponse, HTMLResponse
from fastapi_jwt_auth import AuthJWT
# from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
import datetime
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from schema import *
import bcrypt
import datetime
from routes import auth as auth_router
from routes import listing as listing_router
from config import settings


app = FastAPI(
    title=settings.app_title, docs_url="/docs", openapi_url="/openapi.json",
    description=settings.app_description,
    version=settings.app_version, redoc_url=None
)


class JwtSettings(BaseModel):
    authjwt_secret_key: str = "secret"

@AuthJWT.load_config
def get_config():
    return JwtSettings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*","http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*","http://localhost:3000"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    from db import client
    project_db = client.project
    users_collection = project_db.get_collection("users")
    users = ['mohammad', 'reza', 'mohammadreza']
    for user in users:
        password=bcrypt.hashpw(user.encode('utf-8'), bcrypt.gensalt())
        document = {'userName': user, 'hashedPassword':password, "email":user+"@gmail.com",
         "DoB":"10-10-1950","fullName":user.upper(), "gender":"MALE", "createdAt":datetime.datetime.now()}
        await users_collection.insert_one(document)

@app.get("/")
async def pong():
    return {"msg": "Hello World"}

app.include_router(auth_router.router,  tags=["auth"])
app.include_router(listing_router.router,  tags=["listing"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", reload=True, port=8000)
    # uvicorn main:app --reload --host 0.0.0.0 --port 80
