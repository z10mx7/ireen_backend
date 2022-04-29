from fastapi_jwt_auth import AuthJWT
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from schema import *
import bcrypt
import datetime
from db import client
project_db = client.project
users_collection = project_db.get_collection("users")
router = APIRouter()

@router.get('/api/v3/user/me')
async def me_view(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        if (await users_collection.count_documents({"userName": current_user})) > 0:
            user_json = await users_collection.find_one({"userName": current_user})
        return JSONResponse(status_code=203,content={"email":user_json['email']})  
        
    except Exception as e:
        return JSONResponse(status_code=203,content={"message":"Invalid authorization"})       

@router.post('/api/v3/user/me')
async def me_view(user: Me, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        user_json = await users_collection.find_one({"userName": current_user})
        _id = user_json['_id']
        result = await users_collection.update_one({'_id': _id},  {'$set': {'email': user.email, "updatedAt":datetime.datetime.now()}})
        return JSONResponse(status_code=203,content={"email":user.email})  
        
    except Exception as e:
        return JSONResponse(status_code=203,content={"message":"Invalid authorization"})       
        

@router.post('/api/v3/user/token')
async def signin(user: SignIn, Authorize: AuthJWT = Depends()):
    if user.username is None or user.password is None:
        return JSONResponse(status_code=400, content={"message": "Bad username or password  or credentials is not provided by user"})

    if (await users_collection.count_documents({"userName": user.username})) == 0:
        return JSONResponse(status_code=203,content={"message": "user not exist"})
    else:
        user_json = await users_collection.find_one({"userName": user.username})
        if bcrypt.checkpw(user.password.encode('utf-8'), user_json['hashedPassword']):
            access_token = Authorize.create_access_token(subject=user.username,expires_time=False)
            return JSONResponse(status_code=200,content={"access_token": access_token},)
        else:
            return JSONResponse(status_code=400, content={"message": "Bad password"})
        

@router.put('/api/v3/user/new')
async def signup(user: SignUp, Authorize: AuthJWT = Depends()):
    if user.username is None or user.password is None:
        return JSONResponse(status_code=400, content={"message": "Bad email or password  or password is not provided by user"})

    if user.password != user.repassword:
        return JSONResponse(status_code=203, content={"message": "password and repeat password was not equal"})

    birthday = user.birthday.split("-")[2]
    if int(birthday) <=1940:
        # TODO::  add day and month check 
        return JSONResponse(status_code=203, content={"message": "you should not be too old"})

    if user.gender is None:
        gender = "NOT_SPECIFIED"
    elif user.gender == "FEMALE" or user.gender == "MALE":
        gender = user.gender
    else:
        return JSONResponse(status_code=203, content={"message": "not accepting this gender in this app at this point of time"})

        
    if (await users_collection.count_documents({"userName": user.username})) == 0:
        password=bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        document = {'userName': user.username, 'hashedPassword':password, "email":user.email,
         "DoB":user.birthday,"fullName":user.full_name, "gender":gender, "createdAt":datetime.datetime.now()}
        result = await users_collection.insert_one(document)
        return JSONResponse(status_code=200,content={"message": "user created successfully"})
    else:
        user_json = await users_collection.find_one({"userName": user.username})
        return JSONResponse(status_code=203,content={"message": "user already exist "})
