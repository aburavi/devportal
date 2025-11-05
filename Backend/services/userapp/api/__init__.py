from asyncio.log import logger
from cmath import log
import uuid
from typing import Dict, List, Optional
from urllib import request
from xmlrpc.client import boolean

from sqlalchemy.sql.sqltypes import JSON
from fastapi import FastAPI, status, Header, APIRouter, Depends, HTTPException, File, UploadFile, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime

from aiohttp import ClientSession, ClientTimeout
from starlette.requests import Request

from application import UserappApplication
from models import (
    ModelUser, ModelLogin, ModelRefreshToken, ModelApps, ModelProducts, ModelProductionRequest, ModelBaseCrypto, ModelAppsHistory, ModelApprovedApps
)
from minio import Minio
from minio.error import S3Error
import io
import os
import logging
from .auth_bearer import JWTBearer
from datetime import date
from pydantic import BaseModel, Json
logging.basicConfig(level=logging.DEBUG)

MINIO_DOMAIN = os.getenv("MINIO_DOMAIN", "172.32.233.31")
MINIO_REGION = os.getenv("MINIO_REGION", "id-bandung-POS-1")
MINIO_SECURE = os.getenv("MINIO_SECURE", "False")
MINIO_URL_PATH = os.getenv("MINIO_URL_PATH", "http://172.32.233.31/openapi")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "hv4Hd7xpWnS9qmdzlG")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "MkQDmJrC1slP0dl3Wf")
SANDBOX_SRC_REKENING = os.getenv("SANDBOX_SRC_REKENING", "0060209031245")
SANDBOX_MAX_RATE = os.getenv("SANDBOX_MAX_RATE", "120")
PROJECT_TYPE = os.getenv("PROJECT_TYPE", "sandbox")

class UserappAPI(FastAPI):
    def __init__(self, app: UserappApplication, debug: bool = False, title: str = "POS-OPENAPI", description: str = "", version: str = "0.1.0", openapi_url: str = "/openapi/api/v1/openapi.json", docs_url="/openapi/docs", servers: List[Dict[str, str]] = None) -> None:
        super().__init__(debug=debug, title=title, description=description, version=version, openapi_url=openapi_url, docs_url=docs_url, servers=servers)
        self.app: UserappApplication = app
        users= APIRouter(prefix="/api/v1/user")
        userapps = APIRouter(prefix="/api/v1/apps")
        usercrypto = APIRouter(prefix="/api/v1/basecrypto")
        userproducts = APIRouter(prefix="/api/v1/products")
        userappshistory = APIRouter(prefix="/api/v1/history")
        userproductionrequest = APIRouter(prefix="/api/v1/production")
        upload = APIRouter(prefix="/api/v1/upload")
        sso = APIRouter(prefix="/api/v1/sso")
        approved = APIRouter(prefix="/api/v1/approved")

        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        #self.urlpath = MINIO_URL_PATH
        self.minioClient = Minio(
            MINIO_DOMAIN,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False if MINIO_SECURE == "False" else True,
            region=MINIO_REGION,
        )

        @self.on_event("startup")
        async def startup():
            timeout = ClientTimeout(10)
            self.app.client = ClientSession(timeout=timeout)
            await self.app.repo.initDB()

        @users.post("", dependencies=[Depends(JWTBearer())],
                       summary="Userapp : Create Users",
                       status_code=status.HTTP_201_CREATED,
                       tags=["users"])
        async def new_users(request: ModelUser, token=Depends(JWTBearer())):
             
             result = await self.app.check_userapp(request.username)
             if result["status"] == "02":
                 result1 = await self.app.new_user_keycloak(request, token)
                 if result1["status"] == "00":
                     return JSONResponse(result1, status_code=status.HTTP_200_OK)
                 else:
                     return JSONResponse(result1, status_code=status.HTTP_400_BAD_REQUEST)
             else:
                result2 = {"status":"00","remark":"Already Exist","data":None}
                return JSONResponse(result2, status_code=status.HTTP_400_BAD_REQUEST)

        @users.put("", dependencies=[Depends(JWTBearer())],
                      summary="Userapp : Update Users",
                      status_code=status.HTTP_201_CREATED,
                      tags=["users"])
        async def update_users(request: ModelUser, db_id: str = None):
             result = await self.app.update_users(request, db_id=db_id)
             if result["status"] == "00":
                 return JSONResponse(result, status_code=status.HTTP_200_OK)
             else:
                 return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @users.put("/enable", dependencies=[Depends(JWTBearer())],
                      summary="Userapp : Enable/Disable Users",
                      status_code=status.HTTP_201_CREATED,
                      tags=["users"])
        async def enable_disable_users(user_id: str, enable: bool, token=Depends(JWTBearer())):
             result = await self.app.enable_disable_user_keycloak(user_id, enable, token)
             if result["status"] == "00":
                 return JSONResponse(result, status_code=status.HTTP_200_OK)
             else:
                 return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @users.get("/me", 
                     summary="Userapp: Detail Data users from token",
                     status_code=status.HTTP_200_OK,
                     tags=["users"])
        async def get_users_me(dtoken=Depends(JWTBearer())):
            result = await self.app.login(dtoken)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @users.get("/id/{db_id}", dependencies=[Depends(JWTBearer(['A', 'M']))], 
                      summary="Userapp : Detail Data Users by id",
                     status_code=status.HTTP_200_OK,
                     tags=["users"])
        async def get_users_by_id(db_id: str):
            result = await self.app.get_users_by_id(db_id)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @users.get("/all", dependencies=[Depends(JWTBearer(['A', 'M']))],
                      summary="Userapp : List All Data Users",
                     status_code=status.HTTP_200_OK,
                     tags=["users"])
        async def get_all_users(    
                                    order_by: Optional[str]=None,
                                    keyword: Optional[str]=None,
                                    order_type: Optional[str]='ASC',
                                    limit: Optional[int]=10,
                                    page: Optional[int]=1,
                                    rolecode: Optional[str]=None):
            offset = (page - 1) * limit

            result = await self.app.get_all_users(order_by, keyword, order_type, limit, offset, rolecode)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)
        
        self.include_router(users)

        @userapps.post("", dependencies=[Depends(JWTBearer())],
                       summary="Userapp : Create New Apps",
                       status_code=status.HTTP_201_CREATED,
                       tags=["apps"])
        async def new_apps(apps: ModelApps, token=Depends(JWTBearer())):
            result = await self.app.check_apps(apps.name)
            if result["status"] == "02":
                db_id = str(uuid.uuid4())
                clientid = "".join(str(db_id).split("-"))
                apps.consumer_key = clientid
                srcRek = []
                srcRek.append(SANDBOX_SRC_REKENING)
                if (PROJECT_TYPE == "sandbox"):
                    if (len(apps.src_accounts) == 0):
                        apps.src_accounts = srcRek
                        apps.max_rate = SANDBOX_MAX_RATE
                else:
                    if (len(apps.src_accounts) == 0):
                        return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)
                
                result1 = await self.app.new_client_id_keycloak(apps, token)
                if result1["status"] == "00":
                    return JSONResponse(result1, status_code=status.HTTP_200_OK)
                else:
                    return JSONResponse(result1, status_code=status.HTTP_400_BAD_REQUEST)
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)
 
        @userapps.get("/id/{db_id}", dependencies=[Depends(JWTBearer(['A', 'M']))], 
                    summary="Userapp : Detail Data Apps by id",
                    status_code=status.HTTP_200_OK,
                    tags=["apps"])
        async def get_apps_by_id(db_id: str):
            result = await self.app.get_apps_by_id(db_id)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @userapps.get("/user/{user_id}", dependencies=[Depends(JWTBearer(['T']))], 
                    summary="Userapp : Detail Data Apps by userid",
                    status_code=status.HTTP_200_OK,
                    tags=["apps"])
        async def get_apps_by_userid(user_id: str):
            result = await self.app.get_apps_by_userid(user_id)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @userapps.delete("/id/{db_id}", dependencies=[Depends(JWTBearer(['T']))], 
                    summary="Userapp : Delete Data Apps by id",
                    status_code=status.HTTP_200_OK,
                    tags=["apps"])
        async def delete_apps_by_id(db_id: str):
            result = await self.app.delete_apps_by_id(db_id)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @userapps.get("/all", dependencies=[Depends(JWTBearer(['A', 'M']))],
                    summary="Userapp : All Data Apps",
                    status_code=status.HTTP_200_OK,
                    tags=["apps"])
        async def get_all_apps(
                                    order_by: Optional[str]=None,
                                    keyword: Optional[str]=None,
                                    order_type: Optional[str]='ASC',
                                    limit: Optional[int]=10,
                                    page: Optional[int]=1,
                                    type: Optional[str]=None):
            offset = (page - 1) * limit

            result = await self.app.get_all_apps(order_by, keyword, order_type, limit, offset, type, 'TRUE')
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)
 
        self.include_router(userapps)

        @usercrypto.post("", dependencies=[Depends(JWTBearer())],
                       summary="Userapp : Create Crypto Key Pairs",
                       status_code=status.HTTP_201_CREATED,
                       tags=["crypto"])
        async def new_crypto(request: ModelBaseCrypto):
            result = await self.app.check_usercrypto(request.user_id)
            if result["status"] == "02":
                result1 = await self.app.new_usercrypto(request)
                if result1["status"] == "00":
                    return JSONResponse(result1, status_code=status.HTTP_200_OK)
                else:
                    return JSONResponse(result1, status_code=status.HTTP_400_BAD_REQUEST)
            else:
                result2 = {"status":"00","remark":"Already Exist","data":None}
                return JSONResponse(result2, status_code=status.HTTP_400_BAD_REQUEST)
        
        @usercrypto.get("/user/{user_id}", dependencies=[Depends(JWTBearer())], 
                    summary="Userapp : Data Crypto by userid",
                    status_code=status.HTTP_200_OK,
                    tags=["crypto"])
        async def get_usercrypto_by_userid(user_id: str):
            result = await self.app.check_usercrypto(user_id)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @usercrypto.get("/apps/secret/{consumer_secret}", dependencies=[Depends(JWTBearer())], 
                    summary="Userapp : Data Crypto by Consumer Secret",
                    status_code=status.HTTP_200_OK,
                    tags=["crypto"])
        async def get_appscrypto_by_consumer_secret(consumer_secret: str):
            result = await self.app.check_usercrypto_by_consumer_secret(consumer_secret)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @usercrypto.get("/apps/key/{consumer_key}", dependencies=[Depends(JWTBearer())], 
                    summary="Userapp : Data Crypto by Consumer Key",
                    status_code=status.HTTP_200_OK,
                    tags=["crypto"])
        async def get_appscrypto_by_consumer_key(consumer_key: str):
            result = await self.app.check_usercrypto_by_consumer_key(consumer_key)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @usercrypto.get("/all", dependencies=[Depends(JWTBearer(['A', 'M']))],
                    summary="Userapp : List All Crypto Users",
                    status_code=status.HTTP_200_OK,
                    tags=["crypto"])
        async def get_all_usercrypto(    
                                    order_by: Optional[str]=None,
                                    keyword: Optional[str]=None,
                                    order_type: Optional[str]='ASC',
                                    limit: Optional[int]=10,
                                    page: Optional[int]=1,
                                    isactive: Optional[bool]=None):
            offset = (page - 1) * limit

            result = await self.app.get_all_usercrypto(order_by, keyword, order_type, limit, offset, isactive)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)
 
        self.include_router(usercrypto)

        @userproducts.post("", dependencies=[Depends(JWTBearer())],
                       summary="Userapp : Create Products",
                       status_code=status.HTTP_201_CREATED,
                       tags=["products"])
        async def new_products(request: ModelProducts):
            result = await self.app.new_products(request)
            if result["status"] == "00":
                return JSONResponse(result, status_code=status.HTTP_200_OK)
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)
             
        @userproducts.get("/id/{db_id}", dependencies=[Depends(JWTBearer(['A', 'M']))], 
                      summary="Userapp : Detail Data Product by id",
                     status_code=status.HTTP_200_OK,
                     tags=["products"])
        async def get_products_by_id(db_id: str):
            result = await self.app.get_products_by_id(db_id)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @userproducts.delete("/id/{db_id}", dependencies=[Depends(JWTBearer(['A', 'M']))], 
                      summary="Userapp : Delete Data Products by id",
                     status_code=status.HTTP_200_OK,
                     tags=["products"])
        async def delete_products_by_id(db_id: str):
            result = await self.app.delete_products_by_id(db_id)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @userproducts.get("/all", dependencies=[Depends(JWTBearer(['A', 'M', 'T']))],
                    summary="Userapp : All Data Products",
                    status_code=status.HTTP_200_OK,
                    tags=["products"])
        async def get_all_products(
                                    order_by: Optional[str]=None,
                                    keyword: Optional[str]=None,
                                    order_type: Optional[str]='ASC',
                                    limit: Optional[int]=10,
                                    page: Optional[int]=1):
            offset = (page - 1) * limit

            result = await self.app.get_all_products(order_by, keyword, order_type, limit, offset)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)
 
        self.include_router(userproducts)

        @userproductionrequest.post("", dependencies=[Depends(JWTBearer(['A', 'M']))],
                       summary="Userapp : Create Production Request",
                       status_code=status.HTTP_201_CREATED,
                       tags=["production request"])
        async def new_production_request(request: ModelProductionRequest):
            result = await self.app.new_production_request(request)
            if result["status"] == "00":
                return JSONResponse(result, status_code=status.HTTP_200_OK)
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @userproductionrequest.put("/status", dependencies=[Depends(JWTBearer(['A', 'M']))],
                      summary="Userapp : Update Production Request Status",
                      status_code=status.HTTP_200_OK,
                      tags=["production request"])
        async def update_status_production_request(production_status, db_id: str):
            result = await self.app.update_status_production_request(production_status, db_id)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @userproductionrequest.put("/finalfile", dependencies=[Depends(JWTBearer(['A', 'M', 'T']))],
                      summary="Userapp : Update FinalFile Production Request",
                      status_code=status.HTTP_200_OK,
                      tags=["production request"])
        async def update_production_finalfile(finalfile, db_id: str):
            result = await self.app.update_production_finalfile(finalfile, db_id)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @userproductionrequest.put("/templatefile", dependencies=[Depends(JWTBearer(['A', 'M', 'T']))],
                      summary="Userapp : Update TemplateFile Production Request",
                      status_code=status.HTTP_200_OK,
                      tags=["production request"])
        async def update_production_templatefile(templatefile, db_id: str):
            result = await self.app.update_production_templatefile(templatefile, db_id)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @userproductionrequest.get("/user/{user_id}", dependencies=[Depends(JWTBearer(['T']))], 
                      summary="Userapp : Detail Data Production request by userid",
                     status_code=status.HTTP_200_OK,
                     tags=["production request"])
        async def get_production_requst_by_userid(user_id: str):
            result = await self.app.get_production_request_by_userid(user_id)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @userproductionrequest.get("/user/{user_id}", dependencies=[Depends(JWTBearer(['T']))], 
                      summary="Userapp : Detail Data Production request by userid",
                     status_code=status.HTTP_200_OK,
                     tags=["production request"])
        async def get_production_requst_by_userid(user_id: str):
            result = await self.app.get_production_request_by_userid(user_id)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @userproductionrequest.get("/id/{db_id}", dependencies=[Depends(JWTBearer(['A', 'M']))], 
                      summary="Userapp : Detail Data Production request by id",
                     status_code=status.HTTP_200_OK,
                     tags=["production request"])
        async def get_production_requst_by_id(db_id: str):
            result = await self.app.get_production_request_by_id(db_id)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @userproductionrequest.delete("/id/{db_id}", dependencies=[Depends(JWTBearer(['A', 'M']))], 
                      summary="Userapp : Delete Data Production request by id",
                     status_code=status.HTTP_200_OK,
                     tags=["production request"])
        async def delete_production_request_by_id(db_id: str):
            result = await self.app.delete_production_request_by_id(db_id)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @userproductionrequest.get("/all", dependencies=[Depends(JWTBearer(['A', 'M']))],
                    summary="Userapp : All Data Production request",
                    status_code=status.HTTP_200_OK,
                    tags=["production request"])
        async def get_all_production_request(
                                    order_by: Optional[str]=None,
                                    keyword: Optional[str]=None,
                                    order_type: Optional[str]='ASC',
                                    limit: Optional[int]=10,
                                    page: Optional[int]=1,
                                    request_type: Optional[str]=None):
            offset = (page - 1) * limit

            result = await self.app.get_all_production_request(order_by, keyword, order_type, limit, offset, request_type)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)
 
        self.include_router(userproductionrequest)

        @userappshistory.post("", dependencies=[Depends(JWTBearer())],
                       summary="Userapp : Create Apps History",
                       status_code=status.HTTP_201_CREATED,
                       tags=["apps history"])
        async def new_apps_history(request: ModelAppsHistory):
            result = await self.app.new_apps_history(request)
            if result["status"] == "00":
                return JSONResponse(result, status_code=status.HTTP_200_OK)
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)
             
        @userappshistory.get("/user/{user_id}", dependencies=[Depends(JWTBearer(['A', 'M', 'T']))], 
                      summary="Userapp : Detail Data Apps History by userid",
                     status_code=status.HTTP_200_OK,
                     tags=["apps history"])
        async def get_apps_history_by_userid(user_id: str):
            result = await self.app.get_apps_history_by_userid(user_id)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @userappshistory.get("/id/{db_id}", dependencies=[Depends(JWTBearer(['A', 'M']))], 
                      summary="Userapp : Detail Data Apps History by id",
                     status_code=status.HTTP_200_OK,
                     tags=["apps history"])
        async def get_apps_history_by_id(db_id: str):
            result = await self.app.get_apps_history_by_id(db_id)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @userappshistory.delete("/id/{db_id}", dependencies=[Depends(JWTBearer(['A', 'M']))], 
                      summary="Userapp : Delete Data Apps History by id",
                     status_code=status.HTTP_200_OK,
                     tags=["apps history"])
        async def delete_apps_history_by_id(db_id: str):
            result = await self.app.delete_apps_history_by_id(db_id)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @userappshistory.get("/all", dependencies=[Depends(JWTBearer(['A', 'M']))],
                    summary="Userapp : All Data Apps History",
                    status_code=status.HTTP_200_OK,
                    tags=["apps history"])
        async def get_all_apps_history(
                                    order_by: Optional[str]=None,
                                    keyword: Optional[str]=None,
                                    order_type: Optional[str]='ASC',
                                    limit: Optional[int]=10,
                                    page: Optional[int]=1,
                                    content_type: Optional[str]=None):
            offset = (page - 1) * limit

            result = await self.app.get_all_apps_history(order_by, keyword, order_type, limit, offset, content_type)
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)
 
        self.include_router(userappshistory)

        @upload.post("/image", dependencies=[Depends(JWTBearer())],
            summary="Upload Image",
            status_code=status.HTTP_200_OK,
            tags=["Upload"])
        async def create_upload_image_file(
            file: UploadFile = File(...)
        ):
            contents = await file.read()

            # Upload data.
            ddnow = datetime.now()
            datenow = ddnow.replace(microsecond=0)
            now = datenow.timestamp()
            dnow = str(now).split('.')[0]
            fname = file.filename.split('.')
            uploadresult = self.minioClient.put_object(
                "openapi", "avatar/"+ f'{fname[0]}_{dnow}.{fname[1]}', io.BytesIO(contents), len(contents),
            )
            
            print(
                "created {0} object; etag: {1}, version-id: {2}".format(
                    uploadresult.object_name, uploadresult.etag, uploadresult.version_id,
                ),
            )
            uploadurl = {"url": uploadresult.object_name}
            
            logging.debug(f'upload file result: {uploadresult}')
            if uploadresult.object_name:
                remark = 'success'
                result =  {"status": "00", "remark": remark, "data": uploadurl}
                return JSONResponse(result, status_code=status.HTTP_200_OK)
            else:
                remark = 'failed'
                result =  {"status": "01", "remark": remark, "data": None}
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @upload.post("/document", dependencies=[Depends(JWTBearer())],
            summary="Upload Document",
            status_code=status.HTTP_200_OK,
            tags=["Upload"])
        async def create_upload_document_file(
            file: UploadFile = File(...)
        ):
            contents = await file.read()

            # Upload data.
            ddnow = datetime.now()
            datenow = ddnow.replace(microsecond=0)
            now = datenow.timestamp()
            dnow = str(now).split('.')[0]
            fname = file.filename.split('.')
            uploadresult = self.minioClient.put_object(
                "openapi", "document/"+ f'{fname[0]}_{dnow}.{fname[1]}', io.BytesIO(contents), len(contents),
            )
            
            print(
                "created {0} object; etag: {1}, version-id: {2}".format(
                    uploadresult.object_name, uploadresult.etag, uploadresult.version_id,
                ),
            )
            uploadurl = {"url": uploadresult.object_name}
            
            logging.debug(f'upload file result: {uploadresult}')
            if uploadresult.object_name:
                remark = 'success'
                result =  {"status": "00", "remark": remark, "data": uploadurl}
                return JSONResponse(result, status_code=status.HTTP_200_OK)
            else:
                remark = 'failed'
                result =  {"status": "01", "remark": remark, "data": None}
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        self.include_router(upload)

        @sso.post("/token",
                       summary="SSO : SSO get Token",
                       status_code=status.HTTP_200_OK,
                       tags=["sso"])
        async def sso_login(request: ModelLogin):
            result = await self.app.login_keycloak(request)
            if result["status"] == "00":
                return JSONResponse(result, status_code=status.HTTP_200_OK)
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @sso.post("/refresh-token",
                       summary="SSO : SSO Refresh Token",
                       status_code=status.HTTP_200_OK,
                       tags=["sso"])
        async def sso_refresh_token(request: ModelRefreshToken):
            result = await self.app.refresh_token_keycloak(request)
            if result["status"] == "00":
                return JSONResponse(result, status_code=status.HTTP_200_OK)
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)
         
        self.include_router(sso)

        @approved.post("/apps", dependencies=[Depends(JWTBearer())],
                       summary="Approved : Apps Approved with Source Account",
                       status_code=status.HTTP_200_OK,
                       tags=["approved"])
        async def approved_apps(request: ModelApprovedApps):
            result = await self.app.approved_rekening_to_keycloak(request.consumer_key,request.consumer_secret, request.name, request.src_accounts, request.max_rate)
            if result["status"] == "00":
                return JSONResponse(result, status_code=status.HTTP_200_OK)
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        @approved.get("/all", dependencies=[Depends(JWTBearer())],
                       summary="Approved : List All Apps need Approved",
                       status_code=status.HTTP_200_OK,
                       tags=["approved"])
        async def list_approved_apps(
                                    order_by: Optional[str]=None,
                                    keyword: Optional[str]=None,
                                    order_type: Optional[str]='ASC',
                                    limit: Optional[int]=10,
                                    page: Optional[int]=1,
                                    type: Optional[str]=None):
            offset = (page - 1) * limit

            result = await self.app.get_all_apps(order_by, keyword, order_type, limit, offset, type, 'FALSE')
            if result["status"] == "00":
                return result
            else:
                return JSONResponse(result, status_code=status.HTTP_400_BAD_REQUEST)

        self.include_router(approved)