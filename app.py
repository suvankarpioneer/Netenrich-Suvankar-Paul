from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
import databases
import sqlite3
from sqlalchemy import JSON
import uvicorn
from pydantic import BaseModel
from typing import List, Optional
import asyncio
from fastapi.responses import JSONResponse, RedirectResponse
from config.database import database
from models.user_model import UserModel
from uuid import uuid4
from schemas.user_schema import UserSchema, RegisterSchema, ConnectionRequestSchema, LoginSchema, SearchSchema
# import python jose
from jose import jwt
from fast_autocomplete import AutoComplete
import json

app = FastAPI()
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.on_event("startup")
async def startup():
    print("startup")
    try:  
        await asyncio.wait_for(database(), timeout=60.0)

    except asyncio.TimeoutError as e:
        pass

    except Exception as e:
        print("EXCEPTION", e)


@app.post("/signup")
# take a json request
async def sign_up(request: RegisterSchema):
    try:
        request = request.dict()

        hashed_password = pwd_context.hash(request["password"])

        words = {}
        words[request["username"]] = {}
        print(words)
        # add the word to the txt file
        with open("words.txt", "a") as f:
            f.write("\"" + str(words) + "\"" +"\n")

        user_id = uuid4().hex

        token = jwt.encode({"user_id" : user_id}, "thisisasecretkey")

        user = UserModel(
            user_id=user_id,
            username = request["username"],
            password = hashed_password
        )

        words = {}

        print(user)

        await user.save()


        return JSONResponse(
                status_code=200, 
                content = {
                    "message" : "success",
                    "token" : token
                }
            )
    
    except Exception as e:
        return JSONResponse(
                status_code=500, 
                content = {
                    "message" : "error",
                    "error" : str(e)
                }
            )
    
@app.post("/login")
# take a json request
async def login(request: LoginSchema):
    try:
        request = request.dict()

        user = await UserModel.find_one({"username" : request["username"]})

        if user is None:
            return JSONResponse(
                status_code=500,
                content = {
                    "message": "user doesn't exist"
                }
            )
        
        if not pwd_context.verify(request["password"], user.password):
            return JSONResponse(
                status_code=403,
                content={
                    "message" : "Username or password incorrect"
                }
            )
        
        token = jwt.encode({"user_id" : user.user_id}, "thisisasecretkey")

        return JSONResponse(
                status_code=200,
                content = {
                    "message": "success",
                    "token": token
                }
        )

    except Exception as e:
        return JSONResponse(
                status_code=500, 
                content = {
                    "message" : "error",
                    "error" : str(e)
                }
            )

    
@app.post("/update-profile")
# take a json request
async def update_profile(request: UserSchema):
    try:
        request = request.dict()

        print(request)

        user = await UserModel.find_one({"username" : request["username"]})

        user.first_name = request["first_name"] if request["first_name"] else user.first_name
        user.last_name = request["last_name"] if request["last_name"] else user.last_name
        user.dob = request["dob"] if request["dob"] else user.dob
        user.educational_details = request["educational_details"] if request["educational_details"] else user.educational_details
        # user.email_address = request["email_address"] if request["email_address"] else user.email_address
        user.contact_no = request["contact_no"] if request["contact_no"] else user.contact_no
        user.skills = request["skills"] if request["skills"] else user.skills
        user.internship_details = request["internship_details"] if request["internship_details"] else user.internship_details
        user.yoj = request["yoj"] if request["yoj"] else user.yoj
        user.yop = request["yop"] if request["yop"] else user.yop
        user.department = request["department"] if request["department"] else user.department
        user.course = request["course"] if request["course"] else user.course
        user.current_semeseter = request["current_semeseter"] if request["current_semeseter"] else user.current_semeseter
        user.bio = request["bio"] if request["bio"] else user.bio
        user.address = request["address"] if request["address"] else user.address
        user.hostel = request["hostel"] if request["hostel"] else user.hostel

        await user.save()

        return JSONResponse(
                status_code=200, 
                content = {
                    "message" : "success"
                }
            )
    
    except Exception as e:
        return JSONResponse(
                status_code=500, 
                content = {
                    "message" : "error",
                    "error" : str(e)
                }
            )
    
@app.delete("/delete-profile")
async def delete_profile(request: UserSchema):
    try:
        request = request.dict()

        print(request)

        user = await UserModel.find_one({"username" : request["username"]})

        await user.delete()


        return JSONResponse(
                status_code=200, 
                content = {
                    "message" : "success"
                }
            )
    
    except Exception as e:
        return JSONResponse(
                status_code=500, 
                content = {
                    "message" : "error",
                    "error" : str(e)
                }
            )
    
@app.post("/connection-request")
async def connection_request(request: ConnectionRequestSchema):
    try:
        request = request.dict()

        print(request)

        user = await UserModel.find_one({"username" : request["connection_username"]})
        print(user)

        user.connection_requests.append(request["username"])

        await user.save()

        return JSONResponse(
                status_code=200, 
                content = {
                    "message" : "success"
                }
            )
    
    except Exception as e:
        return JSONResponse(
                status_code=500, 
                content = {
                    "message" : "error",
                    "error" : str(e)
                }
            )
    
@app.post("/accept-request")
async def accept_request(request: ConnectionRequestSchema):
    try:
        request = request.dict()

        print(request)

        user = await UserModel.find_one({"username" : request["username"]})
        print(user)

        user.connections.append(request["connection_username"])
        user.connection_requests.remove(request["connection_username"])

        await user.save()

        return JSONResponse(
                status_code=200, 
                content = {
                    "message" : "success"
                }
            )
    
    except Exception as e:
        return JSONResponse(
                status_code=500, 
                content = {
                    "message" : "error",
                    "error" : str(e)
                }
            )
    
@app.post("/reject-request")
async def reject_request(request: ConnectionRequestSchema):
    try:
        request = request.dict()

        print(request)

        user = await UserModel.find_one({"username" : request["username"]})
        print(user)

        user.connection_requests.remove(request["connection_username"])

        await user.save()

        return JSONResponse(
                status_code=200, 
                content = {
                    "message" : "success"
                }
            )
    
    except Exception as e:
        return JSONResponse(
                status_code=500, 
                content = {
                    "message" : "error",
                    "error" : str(e)
                }
            )
    
@app.post("/remove-connection")
async def remove_connection(request: ConnectionRequestSchema):
    try:
        request = request.dict()

        print(request)

        user = await UserModel.find_one({"username" : request["username"]})
        print(user)

        user.connections.remove(request["connection_username"])

        await user.save()

        return JSONResponse(
                status_code=200, 
                content = {
                    "message" : "success"
                }
            )
    
    except Exception as e:
        return JSONResponse(
                status_code=500, 
                content = {
                    "message" : "error",
                    "error" : str(e)
                }
            )
    
@app.post("/search")
async def search(request: SearchSchema):
    try:
        # read the words.txt file
        file = open("words.txt", "r")
        words = {}
        for line in file:
            json_data = json.loads(line)
           

        # print(words)
    
    except Exception as e:
        return JSONResponse(
                status_code=500, 
                content = {
                    "message" : "error",
                    "error" : str(e)
                }
            )

    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
