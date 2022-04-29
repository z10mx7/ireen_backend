from fastapi_jwt_auth import AuthJWT
from fastapi import  Depends, APIRouter
from models import *
from fastapi.responses import JSONResponse
from schema import *
import datetime
import json
import simplejson
from helpers import listing_helper
from db import client
from bson import json_util

project_db = client.project
users_collection = project_db.get_collection("users")
listing_collection = project_db.get_collection("listing")
router = APIRouter()

async def permission_check(_id, current_user):
    listing_finder = await listing_collection.find_one({"_id": ObjectId(_id)})
    user_json = await users_collection.find_one({"userName": current_user})
    if user_json['_id']!=listing_finder['ownerId']:
        return False
    else:
        return True 

@router.get('/api/v3/listing')
async def list_listing(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        result = []
        async for listing in listing_collection.find({}, {"ownerId":0 }).sort('_id'):
            result.append(listing_helper(listing))
        res = simplejson.dumps(result, default = json_util.default)
        res = json.loads(res)
        return JSONResponse(status_code=203,content=res) 
        
    except Exception as e:
        return JSONResponse(status_code=203,content={"message":"Invalid authorization"})       
      
@router.put('/api/v3/listing/create')
async def create_listing(listing: CreateListing, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        if listing.availableNow:
            if listing.availableNow==1:
                availableNow = True
            else:
                availableNow=False
        else:
            availableNow=False

        user_json = await users_collection.find_one({"userName": current_user})
        _id = user_json['_id']
        document = {'type': listing.ttype, 'availableNow':availableNow, "ownerId":_id,
         "address":listing.address,"createdAt":datetime.datetime.now()}
        result = await listing_collection.insert_one(document)
        return JSONResponse(status_code=203,content={"message":"ok"})          
    except Exception as e:
        return JSONResponse(status_code=203,content={"message":"Invalid authorization"})       
        
@router.get('/api/v3/listing/{idd}')
async def view_listing(idd:str, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        result = []
        listing_json = await listing_collection.find_one({"_id": ObjectId(idd)}, {   "ownerId":0 })
        res = simplejson.dumps(listing_json, default = json_util.default)
        res = json.loads(res)
        return JSONResponse(status_code=203,content=res)  
        
    except Exception as e:
        return JSONResponse(status_code=203,content={"message":"Invalid authorization"})       

@router.post('/api/v3/listing/{_id}')
async def update_listing(listing: CreateListing, _id:str, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        if (await listing_collection.count_documents({"_id": ObjectId(_id)}))>0:
            listing_finder = await listing_collection.find_one({"_id": ObjectId(_id)})
        else:
            return JSONResponse(status_code=203,content={"message":"listing not exist"})  

        user_json = await users_collection.find_one({"userName": current_user})
        if user_json['_id']!=listing_finder['ownerId']:
            return JSONResponse(status_code=203,content={"message":"you are not authorized for this listing"}) 

        if listing.availableNow:
            if listing.availableNow is False:
                availableNow = 0
            else:
                availableNow=1
        else:
            availableNow=0
        result = await listing_collection.update_one({"_id": ObjectId(_id)}, 
         {'$set': {'type': listing.ttype, 'availableNow':availableNow, 
         "address":listing.address,"updatedAt":datetime.datetime.now()}})

        return JSONResponse(status_code=203,content={"message":"ok"})  
        
    except Exception as e:
        return JSONResponse(status_code=203,content={"message":"Invalid authorization"})       

@router.delete('/api/v3/listing/{_id}')
async def delete_listing(_id:str, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        if (await listing_collection.count_documents({"_id": ObjectId(_id)}))>0:
            listing_finder = await listing_collection.find_one({"_id": ObjectId(_id)})
        else:
            return JSONResponse(status_code=203,content={"message":"listing not exist"})  
        user_json = await users_collection.find_one({"userName": current_user})
        if user_json['_id']!=listing_finder['ownerId']:
            return JSONResponse(status_code=203,content={"message":"you are not authorized for this listing"}) 
        listing_json = await listing_collection.find_one_and_delete({"_id": ObjectId(_id)}, {   "ownerId":0 })
        res = simplejson.dumps(listing_json, default = json_util.default)
        res = json.loads(res)
        return JSONResponse(status_code=203,content=res)  
    except Exception as e:
        return JSONResponse(status_code=203,content={"message":"Invalid authorization"})       
        