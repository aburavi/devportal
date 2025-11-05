from array import array
import asyncio
from functools import reduce
import io
from multiprocessing.dummy import Array
import os
import jwt
from datetime import datetime, date
import aiohttp

from typing import Any, Dict, Union
from sqlalchemy.sql.functions import user

from structlog.types import FilteringBoundLogger
from aiohttp import ClientSession

import json
from collections import OrderedDict
from minio import Minio
from minio.error import S3Error

from repository import UserappRepository
from modules.utils import convert_to_basic_filter

from Crypto.PublicKey import RSA

from models import (
    ModelUser,
    ModelApps,
    ModelAppsWithUser, 
    ModelUserPartial,
    ModelProducts,
    ModelProductionRequest,
    ModelProductionRequestWithUser,
    ModelAppsHistory,
    ModelAppsHistoryWithUser,
    ModelBaseCrypto,
    ModelBaseCryptoWithUser,
    ModelLogin,
    ModelRefreshToken
)

MINIO_DOMAIN = os.getenv("MINIO_DOMAIN", "172.32.233.31")
MINIO_URL_PATH = os.getenv("MINIO_URL_PATH", "http://172.32.233.31/openapi")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "hv4Hd7xpWnS9qmdzlG")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "MkQDmJrC1slP0dl3Wf")
SERVICE_KEYCLOAK_URL = os.getenv("SERVICE_KEYCLOAK_URL", "http://172.32.233.18/auth")
SERVICE_KEYCLOAK_CLIENTID = os.getenv("SERVICE_KEYCLOAK_CLIENTID", "adminapi")
SERVICE_KEYCLOAK_CLIENTSECRET = os.getenv("SERVICE_KEYCLOAK_CLIENTSECRET", "c7fad19e-a7f6-4516-b7f2-9701c5649e2b")

class UserappApplication:
    def __init__(self, repo: UserappRepository, logger: FilteringBoundLogger, core_url: str) -> None:
        self.repo: UserappRepository = repo
        self.logger: FilteringBoundLogger = logger
        self.core_url: str = core_url
        self.client: Union[ClientSession, None] = None
        self.urlpath = MINIO_URL_PATH
        self.minioClient = Minio(
            MINIO_DOMAIN,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
        )

    async def reset_database(self):
        await self.repo.resetDB()
        return {"status": "00", "remark": "database reset"}

    def generate_token(self, name, phone, room, appid, appkey, domain, audience, avatar=None):
        if avatar is None:
            avatar = "https://ui-avatars.com/api/?name=" + name
        payload = {
            "context": {
                "user": {
                    "avatar": avatar,
                    "name": name,
                    "phone": phone
                },
            },
            "aud": audience,
            "iss": appid,
            "sub": domain,	
            "room": room,
            "exp": datetime.now().timestamp() + 86400
            #"exp": 1636670657
        }
        self.logger.info("token : " + jwt.encode(payload, appkey, algorithm='HS256'))
        return jwt.encode(payload, appkey, algorithm='HS256')
    
    async def login(self, dtoken: Dict) -> Dict[str, Any]:
        user_id = dtoken.get('sub')
        drequest = ModelUser(
            user_id=user_id,
            username=dtoken.get('preferred_username'),
            firstname=dtoken.get('given_name'),
            lastname=dtoken.get('family_name'),
            email=dtoken.get('email'),
            phone=dtoken.get('telephone'),
            rolecode=dtoken.get('rolecode'),
            isactive=True
        )
        #result = await self.check_userapp(dtoken.get('preferred_username'))
        result = await self.get_userapp_by_id(user_id)
        if result["status"] == "02":
            duser = await self.new_userapp(drequest)
        else:
            duser = await self.update_users(drequest, user_id)
        #--
        if duser["status"] == "00":
            # close last login history
            #await self.close_last_loginhistory(user_id)

            # create new login history
            dlogin = ModelUser(user_id_id=user_id)
            result = await self.new_users(dlogin)
            if result["status"] == "00":
                return {"status": "00", "data": duser["data"], "session_data": result["data"]}
            else:
                return result
        else:
            return duser

#Users
    async def new_users(self, request: ModelUser) -> Dict[str, Any]:
        # self.logger.info("request new userapp : " + str(request))
        result, msgid, remark = await self.repo.new_users(request)
        if result is None:
            return {"status": msgid, "remark": remark, "data": None}
        else:
            return {"status": "00", "remark": remark, "data": result}

    async def update_users(self, request: ModelUser, db_id: str = None):
        result, msgid, remark = await self.repo.update_users(request, db_id)
        if msgid == '00':
            return {"status": "00", "remark": remark, "data": result}
        else:
            return {"status": msgid, "remark": remark, "data": None}
    
    async def check_userapp(self, username: str) -> Dict[str, Any]:
        result, remark = await self.repo.check_userapp(username)
        self.logger.info("result: " + remark)
        if result:
            return {"status": "00", "remark": remark, "data": result} 
        else:
            return {"status": "02", "remark": remark, "data": None}

    async def get_users_by_id(self, id: str) -> Dict[str, Any]:
        result, remark = await self.repo.get_users_by_db_id(id)
        if result:
            return {"status": "00", "remark": remark, "data": result.EntityUser}
        else:
            return {"status": "00", "remark": remark, "data": None}

    async def get_all_users(self, 
        order_by: str, keyword: str, order_type: str, 
        limit: int, offset: int, 
        rolecode: str = None) -> Dict[str, Any]:
        
        basic_filter = convert_to_basic_filter(rolecode=rolecode)
        result, remark = await self.repo.get_all_profile(order_by, keyword, order_type, limit, offset, basic_filter)
        if (result or remark == 'Success'):
            return {"status": "00", "remark": remark, "data": result}
        else:
            return {"status": "02", "remark": remark, "data": None}
                      
    async def get_all_users_by_rolecode(self, 
        rolecode: str,
        order_by: str, keyword: str, order_type: str, 
        limit: int, offset: int) -> Dict[str, Any]:
        result, remark = await self.repo.get_all_users_by_rolecode(rolecode, order_by, keyword, order_type, limit, offset)
        if len(result) < 1:
            return {"status": "02", "remark": remark, "data": None}
        else:
            return {"status": "00", "remark": remark, "data": result}

    async def new_user_keycloak(self, user: ModelUser, token: str) -> Dict[str, Any]:        
        url=f"{SERVICE_KEYCLOAK_URL}/admin/realms/openapi/users"
        headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token,
                }
        request = {
            "createdTimestamp": round(datetime.now().timestamp() * 1000),
            "username": user.username,
            "enabled": True,
            "totp": False,
            "emailVerified": False,
            "firstName": user.firstname,
            "lastName": user.lastname,
            "email": user.email,
            "disableableCredentialTypes": [],
            "requiredActions": [],
            "notBefore": 0,
            "groups": ["tenant"],
            "access": {
                "manageGroupMembership": True,
                "view": True,
                "mapRoles": True,
                "impersonate": True,
                "manage": True
            },
            "attributes": {
                "rolecode":"T",
                "company":user.company,
                "address":user.address,
                "avatar":user.avatar,
                "ph": user.phone
            },
            "realmRoles": [	"tenant" ],
            "clientRoles": {
                "adminapi": ["tenant"]
            },
            "credentials":[{"type":"password", "value":user.password, "temporary":False}]
        }
        djson = json.dumps(request)
        async with self.client.post(url, data=djson, headers=headers) as resp:
            response = await resp.text()
            self.logger.info("Keycloak: create user response", response=response)
            if resp.status==201:
                result, msgid, remark = await self.repo.new_users(user)
                if result is None:
                    return {"status": msgid, "remark": remark, "data": None}
                else:
                    result1 = await self.set_user_id_keycloak(user, token)
                    if result1 is None:
                        msgid='02'
                        remark='Failed to Fetch data'
                        return {"status": msgid, "remark": remark, "data": None}
                    else:
                        return {"status": "00", "remark": "Success update user_id", "data": result.to_dict()}
            else:
                msgid='02'
                remark='Failed to Fetch data'
                return {"status": msgid, "remark": remark, "data": None}
        
    async def set_user_id_keycloak(self, user: ModelUser, token: str) -> Dict[str, Any]:        
        url=f"{SERVICE_KEYCLOAK_URL}/admin/realms/openapi/users?username={user.username}&exact=true"
        headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token,
                }
        request = {
        }
        try:
            async with self.client.get(url, headers=headers) as resp:
                response = await resp.json()
                self.logger.info("Keycloak: get username response", response=response[0])
                if resp.status==200:
                    user.user_id = response[0].get('id')
                    result, msgId, remark = await self.repo.update_users_by_username(user)
                    if result is None:
                        return {"status": msgId, "remark": remark, "data": None}
                    else:
                        return {"status": "00", "remark": "Success create user", "data": result}
                else:
                    msgid='02'
                    remark='Failed to Fetch data'
                    return {"status": msgid, "remark": remark, "data": None}
        except asyncio.TimeoutError:
            remark = "Request to keycloak: create user service timeout"
            self.logger.warn(remark, url=url, method="POST", body=request)
            result = {"status": "02", "remark": remark, "data": None}
            return result
        except Exception as e:
            remark = "Request to keycloak: create user service error"
            self.logger.error(remark, error=f"{repr(e)} | {str(e)}")
            result = {"status": "02", "remark": remark, "data": None}
            return result

    async def enable_disable_user_keycloak(self, user_id: str, enable: bool, token: str) -> Dict[str, Any]:        
        url=f"{SERVICE_KEYCLOAK_URL}/admin/realms/openapi/users/{user_id}"
        headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token,
                }
        request = {
            "enabled": enable
        }
        djson = json.dumps(request)
        try:
            async with self.client.put(url, data=djson, headers=headers) as resp:
                response = await resp.json()
                self.logger.info("Keycloak: enable/disable user response", response=response)
                if resp.status==200:
                    result1, msgid1, remark1 = await self.repo.delete_user_by_userid(user_id)
                    if msgid1 == '00':
                        return {"status": "00", "remark": remark1, "data": result1.to_dict()}
                    else:
                        return {"status": msgid1, "remark": remark1, "data": None}

                    msgid='00'
                    remark='Success'
                    return {"status": msgid, "remark": remark, "data": response}
                else:
                    msgid='02'
                    remark='Failed to Fetch data'
                    return {"status": msgid, "remark": remark, "data": result.to_dict()}
                
        except asyncio.TimeoutError:
            remark = "Request to keycloak: update enable user service timeout"
            self.logger.warn(remark, url=url, method="POST", body=request)
            result = {"status": "02", "remark": remark, "data": None}
            return result
        except Exception as e:
            remark = "Request to keycloak: update enable user service error"
            self.logger.error(remark, error=f"{repr(e)} | {str(e)}")
            result = {"status": "02", "remark": remark, "data": None}
            return result
#Crypto
    async def new_usercrypto(self, request: ModelBaseCrypto) -> Dict[str, Any]:
        # self.logger.info("request new apps : " + str(request))
        key = RSA.generate(2048)
        privateKey = key.export_key()
        publicKey = key.publickey().export_key()
        dnow = datetime.now()

        request = ModelBaseCrypto(
            user_id= request.user_id,
            public_key= publicKey,
            private_key= privateKey,
            expired_at= dnow.replace(dnow.year+1),
            isactive= True,
        )

        result, msgid, remark = await self.repo.new_usercrypto(request)
        if result is None:
            return {"status": msgid, "remark": remark, "data": None}
        else:
            return {"status": "00", "remark": remark, "data": result.to_dict()}

    async def check_usercrypto(self, user_id: str) -> Dict[str, Any]:
        result, remark = await self.repo.check_usercrypto(user_id)
        self.logger.info("result: " + remark)
        if result:
            return {"status": "00", "remark": remark, "data": result.EntityBaseCrypto} 
        else:
            return {"status": "02", "remark": remark, "data": None}

    async def check_usercrypto_by_consumer_secret(self, consumer_secret: str) -> Dict[str, Any]:
        result, remark = await self.repo.check_apps_by_consumer_secret(consumer_secret)
        if result:
            result2, remark2 = await self.repo.check_usercrypto(result.EntityApps.user_id)
            if result2:
                return {"status": "00", "remark": remark2, "data": result2.EntityBaseCrypto} 
            else:
                return {"status": "02", "remark": remark2, "data": None}    
        else:
            return {"status": "02", "remark": remark, "data": None}

    async def check_usercrypto_by_consumer_key(self, consumer_key: str) -> Dict[str, Any]:
        result, remark = await self.repo.check_apps_by_consumer_key(consumer_key)
        if result:
            result2, remark2 = await self.repo.check_usercrypto(result.EntityApps.user_id)
            if result2:
                ddata = {"client_secret":result.EntityApps.consumer_secret, "public_key": result2.EntityBaseCrypto.public_key, "private_key": result2.EntityBaseCrypto.private_key}
                return {"status": "00", "remark": remark2, "data": ddata} 
            else:
                return {"status": "02", "remark": remark2, "data": None}    
        else:
            return {"status": "02", "remark": remark, "data": None}

    async def get_all_usercrypto(self, 
        order_by: str, keyword: str, order_type: str, 
        limit: int, offset: int, 
        isactive: bool = None) -> Dict[str, Any]:
        
        basic_filter = convert_to_basic_filter(type=type)
        result, remark = await self.repo.get_all_usercrypto(order_by, keyword, order_type, limit, offset, basic_filter)
        if len(result) > 0 :
            dresult = []
            for res in result:
                result1, remark1 = await self.repo.get_users_by_user_id(res.user_id)
                if result1:
                    ModUser = ModelUserPartial(
                        firstname=result1.EntityUser.firstname,
                        lastname=result1.EntityUser.lastname,
                        email=result1.EntityUser.email,
                        phone=result1.EntityUser.phone,
                        company=result1.EntityUser.company,
                        address=result1.EntityUser.address,
                        avatar=result1.EntityUser.avatar,
                    )
                    model_crypto_with_user = ModelBaseCryptoWithUser(
                        user=ModUser,
                        public_key=res.public_key,
                        private_key=res.private_key,
                        expired_at=res.expired_at,
                        isactive=res.isactive,
                    )
                    dresult.append(model_crypto_with_user)
                else:
                    model_crypto_with_user = ModelBaseCryptoWithUser(
                        user=None,
                        public_key=res.public_key,
                        private_key=res.private_key,
                        expired_at=res.expired_at,
                        isactive=res.isactive,
                    )
                    dresult.append(model_crypto_with_user)
                
            return {"status": "00", "remark": remark1, "data": dresult}
        else:
            return {"status": "00", "remark": remark, "data": None}

#Apps 
    async def new_apps(self, request: ModelApps) -> Dict[str, Any]:
        # self.logger.info("request new apps : " + str(request))
        result, msgid, remark = await self.repo.new_apps(request)
        if result is None:
            return {"status": msgid, "remark": remark, "data": None}
        else:
            return {"status": "00", "remark": remark, "data": result.to_dict()}

    async def check_apps(self, name: str) -> Dict[str, Any]:
        result, remark = await self.repo.check_apps(name)
        self.logger.info("result: " + remark)
        if result:
            return {"status": "00", "remark": remark, "data": result} 
        else:
            return {"status": "02", "remark": remark, "data": None}

    async def delete_apps_by_id(self, db_id: str = None):
        result, msgid, remark = await self.delete_client_id_keycloak(db_id)
        if msgid == '00':
            result1, msgid1, remark1 = await self.repo.delete_apps_by_id(db_id)
            if msgid1 == '00':
                return {"status": "00", "remark": remark1, "data": result1}
            else:
             return {"status": msgid1, "remark": remark1, "data": None}
        else:
            return {"status": msgid, "remark": remark, "data": result1}

    async def get_apps_by_userid(self, user_id: str) -> Dict[str, Any]:
        result, remark = await self.repo.get_apps_by_userid(user_id)
        if result:
            return {"status": "00", "remark": remark, "data": result}
        else:
            return {"status": "00", "remark": remark, "data": None}

    async def get_apps_by_id(self, id: str) -> Dict[str, Any]:
        result, remark = await self.repo.get_apps_by_db_id(id)
        if result:
            return {"status": "00", "remark": remark, "data": result.EntityApps}
        else:
            return {"status": "00", "remark": remark, "data": None}

    async def get_all_apps(self, 
        order_by: str, keyword: str, order_type: str, 
        limit: int, offset: int, 
        type: str = None,
        isactive: str = None) -> Dict[str, Any]:
        
        basic_filter = convert_to_basic_filter(type=type, isactive=isactive)
        result, remark = await self.repo.get_all_apps(order_by, keyword, order_type, limit, offset, basic_filter)
        if len(result) > 0 :
            dresult = []
            for res in result:
                result1, remark1 = await self.repo.get_users_by_user_id(res.user_id)
                if result1:
                    ModUser = ModelUserPartial(
                        firstname=result1.EntityUser.firstname,
                        lastname=result1.EntityUser.lastname,
                        email=result1.EntityUser.email,
                        phone=result1.EntityUser.phone,
                        company=result1.EntityUser.company,
                        address=result1.EntityUser.address,
                        avatar=result1.EntityUser.avatar,
                    )
                    model_apps_with_user = ModelAppsWithUser(
                        user=ModUser,
                        name=res.name,
                        consumer_key=res.consumer_key,
                        consumer_secret=res.consumer_secret,
                        type=res.type,
                        src_accounts=res.src_accounts,
                        products=res.products,
                        isactive=res.isactive,
                    )
                    dresult.append(model_apps_with_user)
                else:
                    model_apps_with_user = ModelAppsWithUser(
                        user=None,
                        name=res.name,
                        consumer_key=res.consumer_key,
                        consumer_secret=res.consumer_secret,
                        type=res.type,
                        src_accounts=res.src_accounts,
                        products=res.products,
                        isactive=res.isactive,
                    )
                    dresult.append(model_apps_with_user)
                
            return {"status": "00", "remark": remark1, "data": dresult}
        else:
            return {"status": "00", "remark": remark, "data": None}          
    
    async def get_all_apps_by_type(self, 
        type: str,
        order_by: str, keyword: str, order_type: str, 
        limit: int, offset: int) -> Dict[str, Any]:
        result, remark = await self.repo.get_all_apps_by_type(type, order_by, keyword, order_type, limit, offset)
        if len(result) < 1:
            return {"status": "02", "remark": remark, "data": None}
        else:
            return {"status": "00", "remark": remark, "data": result}

    async def new_client_id_keycloak(self, apps: ModelApps, token: str) -> Dict[str, Any]:        
        url=f"{SERVICE_KEYCLOAK_URL}/admin/realms/openapi/clients"
        headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token,
                }
        request = {
            "clientId": apps.consumer_key,
            "name": apps.name,
            "adminUrl": "",
            "alwaysDisplayInConsole": False,
            "access": {
                "view": True,
                "configure": True,
                "manage": True
            },
            "attributes": {},
            "authenticationFlowBindingOverrides" : {},
            "authorizationServicesEnabled": True,
            "bearerOnly": False,
            "directAccessGrantsEnabled": True,
            "enabled": True,
            "protocol": "openid-connect",
            "description": "rest-openapi",

            "rootUrl": "${authBaseUrl}",
            "baseUrl": "/realms/openapi/account/",
            "surrogateAuthRequired": False,
            "clientAuthenticatorType": "client-secret",
            "defaultRoles": [
                "manage-account",
                "view-profile"
            ],
            "redirectUris": ["/*"],
            "webOrigins": ["*"],
            "notBefore": 0,
            "consentRequired": False,
            "standardFlowEnabled": False,
            "implicitFlowEnabled": False,
            "serviceAccountsEnabled": True,
            "publicClient": False,
            "frontchannelLogout": False,
            "fullScopeAllowed": False,
            "nodeReRegistrationTimeout": 0,
            "defaultClientScopes": [
                "web-origins",
                "role_list",
                "profile",
                "roles",
                "email"
            ],
            "optionalClientScopes": [
                "address",
                "phone",
                "offline_access",
                "microprofile-jwt"
            ]
        }
        djson = json.dumps(request)
        async with self.client.post(url, data=djson, headers=headers) as resp:
            response = await resp.text()
            self.logger.info("Keycloak: create client_id response", response=response)
            if resp.status==201:
                result1 = await self.repo.new_apps(apps)
                if result1 is None:
                    return {"status": '02', "remark": 'Failed create Apps', "data": None}
                else:
                    result2 = await self.get_client_id_keycloak(apps.consumer_key, token)
                    if result2 is None:
                        return {"status": "02", "remark": "Failed to fetch id client_id", "data": None}
                    else:
                        self.logger.info("get_client_id_keycloak result2: " + result2['data'])
                        result3 = await self.get_client_secret_keycloak(result2["data"], token)
                        if result3 is None:
                            return {"status": '02', "remark": 'Failed to get Secret', "data": None}
                        else:
                            scopes=[]
                            uris=[]
                            s=''
                            for scope in apps.products:
                                dscope = scope.replace('/', '-')
                                scopes.append(f'scopes-{dscope}')

                            for uri in apps.products:
                                uris.append(f'/{apps.type}{uri}')
                            
                            dclient_id = apps.consumer_key
                            dclient_secret = result3["data"]
                            dresult4 = await self.login_keycloak_with_client_credentials(dclient_id, dclient_secret)
                            if dresult4:
                                result5 = await self.new_managed_resource_keycloak(apps.type, apps.consumer_key, apps.src_accounts, apps.max_rate, scopes, uris, dresult4['data']['access_token'] )
                                if result5:
                                    result6 = await self.repo.update_apps_secret(result3["data"], apps.consumer_key )
                                    if result6:
                                        return {"status": '00', "remark": 'Success', "data": None}
                                    else:
                                        return {"status": '02', "remark": 'failed to update secret', "data": None}
                                else:
                                    return {"status": '02', "remark": 'Failed to create managed resource', "data": None}
                            else:
                                    return {"status": '02', "remark": 'Failed to login Credentials', "data": None}
            else:
                msgid='02'
                remark='Failed to fetch data'
                return {"status": msgid, "remark": remark, "data": None} 
    
    async def login_keycloak_with_client_credentials(self, client_id, client_secret: str) -> Dict[str, Any]:        
        url=f"{SERVICE_KEYCLOAK_URL}/realms/openapi/protocol/openid-connect/token"
        headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                }
        data = aiohttp.FormData()
        data.add_field('client_id',client_id)
        data.add_field('client_secret',client_secret)
        data.add_field('grant_type','client_credentials')
        try:
            async with self.client.post(url, data=data, headers=headers) as resp:
                response = await resp.json()
                self.logger.info("Keycloak: login with client_credentials", response=response)
                if resp.status==200:
                    msgid='00'
                    remark='Success'
                    return {"status": msgid, "remark": remark, "data": response} 
                else:
                    msgid='02'
                    remark='Failed to fetch data'
                    return {"status": msgid, "remark": remark, "data": None} 

        except asyncio.TimeoutError:
            remark = "Request to keycloak service timeout"
            self.logger.warn(remark, url=url, method="POST", body=None)
            result = {"status": "02", "remark": remark, "data": None}
            return result
        except Exception as e:
            remark = "Request to keycloak service error"
            self.logger.error(remark, error=f"{repr(e)} | {str(e)}")
            result = {"status": "02", "remark": remark, "data": None}
            return result


    async def delete_client_id_keycloak(self, db_id: str, token: str) -> Dict[str, Any]:        
        url=f"{SERVICE_KEYCLOAK_URL}/admin/realms/openapi/clients/{db_id}"
        headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                }

        request = {
        }

        try:
            async with self.client.delete(url, headers=headers) as resp:
                response = await resp.json()
                self.logger.info("Keycloak: create client_id response", response=response)

                if resp.status==200:
                    msgid='00'
                    remark='Success'
                    return {"status": msgid, "remark": remark, "data": None} 
                else:
                    msgid='02'
                    remark='Failed to fetch data'
                    return {"status": msgid, "remark": remark, "data": None} 

        except asyncio.TimeoutError:
            remark = "Request to keycloak service timeout"
            self.logger.warn(remark, url=url, method="POST", body=request)
            result = {"status": "02", "remark": remark, "data": None}
            return result
        except Exception as e:
            remark = "Request to keycloak service error"
            self.logger.error(remark, error=f"{repr(e)} | {str(e)}")
            result = {"status": "02", "remark": remark, "data": None}
            return result


    async def get_client_id_keycloak(self, client_id: str, token: str) -> Dict[str, Any]:        
        url=f"{SERVICE_KEYCLOAK_URL}/admin/realms/openapi/clients?clientId={client_id}"
        headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                }
        
        try:
            async with self.client.get(url, headers=headers) as resp:
                response = await resp.json()
                self.logger.info("Keycloak: client_id response", response=response)
                if resp.status==200:
                    msgid='00'
                    remark='Success'
                    return {"status": msgid, "remark": remark, "data": response[0]["id"]}
                else:
                    msgid='02'
                    remark='Failed to fetch data'
                    return {"status": msgid, "remark": remark, "data": response[0]["id"]}

        except asyncio.TimeoutError:
            remark = "Request to keycloak client_id service timeout"
            self.logger.warn(remark, url=url, method="GET")
            result = {"status": "02", "remark": remark, "data": None}
            return result
        except Exception as e:
            remark = "Request to keycloak client_id service error"
            self.logger.error(remark, error=f"{repr(e)} | {str(e)}")
            result = {"status": "02", "remark": remark, "data": None}
            return result

    async def get_client_secret_keycloak(self, id: str, token: str) -> Dict[str, Any]:        
        url=f"{SERVICE_KEYCLOAK_URL}/admin/realms/openapi/clients/{id}/client-secret"
        headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                }
        try:
            async with self.client.get(url, headers=headers) as resp:
                response = await resp.json()
                self.logger.info("Keycloak: client_secret response", response=response)
                if resp.status==200:
                    msgid='00'
                    remark='Success'
                    return {"status": msgid, "remark": remark, "data": response.pop("value")}
                else:
                    msgid='02'
                    remark='Failed to fetch data'
                    return {"status": msgid, "remark": remark, "data": response[0].pop("id")}
                    
        except asyncio.TimeoutError:
            remark = "Request to keycloak client_secret service timeout"
            self.logger.warn(remark, url=url, method="GET")
            result = {"status": "02", "remark": remark, "data": None}
            return result
        except Exception as e:
            remark = "Request to keycloak client_secret service error"
            self.logger.error(remark, error=f"{repr(e)} | {str(e)}")
            result = {"status": "02", "remark": remark, "data": None}
            return result

#Products
    async def new_products(self, request: ModelProducts) -> Dict[str, Any]:
        # self.logger.info("request new products : " + str(request))
        result, msgid, remark = await self.repo.new_products(request)
        if result is None:
            return {"status": msgid, "remark": remark, "data": None}
        else:
            return {"status": "00", "remark": remark, "data": result.to_dict()}

    async def delete_products_by_id(self, db_id: str = None):
        result, msgid, remark = await self.repo.delete_products_by_id(db_id)
        if msgid == '00':
            return {"status": "00", "remark": remark, "data": result}
        else:
            return {"status": msgid, "remark": remark, "data": None}

    async def get_products_by_id(self, id: str) -> Dict[str, Any]:
        result, remark = await self.repo.get_products_by_db_id(id)
        if result:
            return {"status": "00", "remark": remark, "data": result.EntityProducts}
        else:
            return {"status": "00", "remark": remark, "data": None}

    async def get_all_products(self, 
        order_by: str, keyword: str, order_type: str, 
        limit: int, offset: int, 
        type: str = None) -> Dict[str, Any]:
        
        basic_filter = convert_to_basic_filter(type=type)
        result, remark = await self.repo.get_all_products(order_by, keyword, order_type, limit, offset, basic_filter)
        return {"status": "00", "remark": remark, "data": result}            

#Production Request    
    async def new_production_request(self, request: ModelProductionRequest) -> Dict[str, Any]:
        # self.logger.info("request new products : " + str(request))
        result, msgid, remark = await self.repo.new_production_request(request)
        if result is None:
            return {"status": msgid, "remark": remark, "data": None}
        else:
            hrequest = ModelAppsHistory(
                user_id=request.user_id,
                content='New Production Request',
                content_type='production_request',
                description=request.requested_by + ':' + request.request_type + ':' + request.template_file + ':' + request.final_file ,
                status=request.status,
                approved_at=request.approved_at.strftime('%Y-%m-%d %H:%M:%S'),
                approved_by=request.approved_by,
                isactive=request.isactive,
            )
            result1, msgid1, remark1 = await self.repo.new_apps_history(hrequest)
            if result1 is None:
                self.logger.info("insert to new_apps_history failed with remark: " + remark1)
            else:
                self.logger.info("insert to new_apps_history with remark: " + remark1)

            return {"status": "00", "remark": remark, "data": result.to_dict()}

    async def update_status_production_request(self, status, db_id: str = None):
        result, msgid, remark = await self.repo.update_status_production_request(status, db_id)
        if msgid == '00':
            hrequest = ModelAppsHistory(
                user_id=result.EntityProductionRequest.user_id,
                content='Update Status Production Request',
                content_type='production_request',
                description=result.EntityProductionRequest.requested_by + ':' + result.EntityProductionRequest.request_type + ':' + result.EntityProductionRequest.template_file + ':' + result.EntityProductionRequest.final_file ,
                status=result.EntityProductionRequest.status,
                approved_at=result.EntityProductionRequest.approved_at.strftime('%Y-%m-%d %H:%M:%S'),
                approved_by=result.EntityProductionRequest.approved_by,
                isactive=result.EntityProductionRequest.isactive,
            )
            result1, msgid1, remark1 = await self.repo.new_apps_history(hrequest)
            if result1 is None:
                self.logger.info("insert to new_apps_history failed with remark: " + remark1)
            else:
                self.logger.info("insert to new_apps_history with remark: " + remark1)

            return {"status": "00", "remark": remark, "data": result.EntityProductionRequest}
        else:
            return {"status": msgid, "remark": remark, "data": None}

    async def update_production_finalfile(self, finalfile, db_id: str = None):
        result, msgid, remark = await self.repo.update_production_finalfile(finalfile, db_id)
        if msgid == '00':
            hrequest = ModelAppsHistory(
                user_id=result.EntityProductionRequest.user_id,
                content='Update Final File Production Request',
                content_type='production_request',
                description=result.EntityProductionRequest.requested_by + ':' + result.EntityProductionRequest.request_type + ':' + result.EntityProductionRequest.template_file + ':' + result.EntityProductionRequest.final_file ,
                status=result.EntityProductionRequest.status,
                approved_at=result.EntityProductionRequest.approved_at.strftime('%Y-%m-%d %H:%M:%S'),
                approved_by=result.EntityProductionRequest.approved_by,
                isactive=result.EntityProductionRequest.isactive,
            )
            result1, msgid1, remark1 = await self.repo.new_apps_history(hrequest)
            if result1 is None:
                self.logger.info("insert to new_apps_history failed with remark: " + remark1)
            else:
                self.logger.info("insert to new_apps_history with remark: " + remark1)

            return {"status": "00", "remark": remark, "data": result.EntityProductionRequest}
        else:
            return {"status": msgid, "remark": remark, "data": None}

    async def update_production_templatefile(self, templatefile, db_id: str = None):
        result, msgid, remark = await self.repo.update_production_templatefile(templatefile, db_id)
        if msgid == '00':
            hrequest = ModelAppsHistory(
                user_id=result.EntityProductionRequest.user_id,
                content='Update Template File Production Request',
                content_type='production_request',
                description=result.EntityProductionRequest.requested_by + ':' + result.EntityProductionRequest.request_type + ':' + result.EntityProductionRequest.template_file + ':' + result.EntityProductionRequest.final_file ,
                status=result.EntityProductionRequest.status,
                approved_at=result.EntityProductionRequest.approved_at.strftime('%Y-%m-%d %H:%M:%S'),
                approved_by=result.EntityProductionRequest.approved_by,
                isactive=result.EntityProductionRequest.isactive,
            )
            result1, msgid1, remark1 = await self.repo.new_apps_history(hrequest)
            if result1 is None:
                self.logger.info("insert to new_apps_history failed with remark: " + remark1)
            else:
                self.logger.info("insert to new_apps_history with remark: " + remark1)

            return {"status": "00", "remark": remark, "data": result.EntityProductionRequest}
        else:
            return {"status": msgid, "remark": remark, "data": None}

    async def delete_production_request_by_id(self, db_id: str = None):
        result, msgid, remark = await self.repo.delete_production_request_by_id(db_id)
        if msgid == '00':
            hrequest = ModelAppsHistory(
                user_id=result.user_id,
                content='Delete Production Request',
                content_type='production_request',
                description=result.requested_by + ':' + result.request_type + ':' + result.template_file + ':' + result.final_file ,
                status=result.status,
                approved_at=result.approved_at.strftime('%Y-%m-%d %H:%M:%S'),
                approved_by=result.approved_by,
                isactive=result.isactive,
            )
            result1, msgid1, remark1 = await self.repo.new_apps_history(hrequest)
            if result1 is None:
                self.logger.info("insert to new_apps_history failed with remark: " + remark1)
            else:
                self.logger.info("insert to new_apps_history with remark: " + remark1)

            return {"status": "00", "remark": remark, "data": result}
        else:
            return {"status": msgid, "remark": remark, "data": None}

    async def get_production_request_by_id(self, id: str) -> Dict[str, Any]:
        result, remark = await self.repo.get_production_request_by_db_id(id)
        if result:
            return {"status": "00", "remark": remark, "data": result.EntityProductionRequest}
        else:
            return {"status": "00", "remark": remark, "data": None}

    async def get_production_request_by_userid(self, user_id: str) -> Dict[str, Any]:
        result, remark = await self.repo.get_production_request_by_userid(user_id)
        if result:
            return {"status": "00", "remark": remark, "data": result}
        else:
            return {"status": "00", "remark": remark, "data": None}

    async def get_all_production_request(self, 
        order_by: str, keyword: str, order_type: str, 
        limit: int, offset: int, 
        request_type: str = None) -> Dict[str, Any]:
        
        basic_filter = convert_to_basic_filter(request_type=request_type)
        result, remark = await self.repo.get_all_production_request(order_by, keyword, order_type, limit, offset, basic_filter)
        if len(result) >= 0 :
            dresult = []
            for res in result:
                result1, remark1 = await self.repo.get_users_by_user_id(res.user_id)
                self.logger.info("get_all_production_request : " + remark1)
                if result1:
                    ModUser = ModelUserPartial(
                        firstname=result1.EntityUser.firstname,
                        lastname=result1.EntityUser.lastname,
                        email=result1.EntityUser.email,
                        phone=result1.EntityUser.phone,
                        company=result1.EntityUser.company,
                        address=result1.EntityUser.address,
                        avatar=result1.EntityUser.avatar,
                    )
                    model_production_request_with_user = ModelProductionRequestWithUser(
                        db_id = str(res.db_id),
                        user=ModUser,
                        requested_by=res.requested_by,
                        request_type=res.request_type,
                        status=res.status,
                        template_file=res.template_file,
                        final_file=res.final_file,
                        approved_at=res.approved_at.strftime("%Y-%m-%d %H:%M:%S"),
                        approved_by=res.approved_by,
                        isactive=res.isactive,
                    )
                    dresult.append(model_production_request_with_user)
                else:
                    model_production_request_with_user = ModelProductionRequestWithUser(
                        user=None,
                        requested_by=res.requested_by,
                        request_type=res.request_type,
                        status=res.status,
                        template_file=res.template_file,
                        final_file=res.final_file,
                        approved_at=res.res.approved_at.strftime("%Y-%m-%d %H:%M:%S"),
                        approved_by=res.approved_by,
                        isactive=res.isactive,
                    )
                    dresult.append(model_production_request_with_user)
                
            return {"status": "00", "remark": remark, "data": dresult}
        else:
            return {"status": "00", "remark": remark, "data": None}            

#AppsHistory     
    async def new_apps_history(self, request: ModelAppsHistory) -> Dict[str, Any]:
        # self.logger.info("request new products : " + str(request))
        result, msgid, remark = await self.repo.new_apps_history(request)
        if result is None:
            return {"status": msgid, "remark": remark, "data": None}
        else:
            return {"status": "00", "remark": remark, "data": result.to_dict()}

    async def delete_apps_history_by_id(self, db_id: str = None):
        result, msgid, remark = await self.repo.delete_apps_history_by_id(db_id)
        if msgid == '00':
            return {"status": "00", "remark": remark, "data": result}
        else:
            return {"status": msgid, "remark": remark, "data": None}

    async def get_apps_history_by_userid(self, user_id: str) -> Dict[str, Any]:
        result, remark = await self.repo.get_apps_history_by_userid(user_id)
        if result:
            return {"status": "00", "remark": remark, "data": result}
        else:
            return {"status": "00", "remark": remark, "data": None}

    async def get_apps_history_by_id(self, id: str) -> Dict[str, Any]:
        result, remark = await self.repo.get_apps_history_by_db_id(id)
        if result:
            return {"status": "00", "remark": remark, "data": result.EntityAppsHistory}
        else:
            return {"status": "00", "remark": remark, "data": None}

    async def get_all_apps_history(self, 
        order_by: str, keyword: str, order_type: str, 
        limit: int, offset: int, 
        content_type: str = None) -> Dict[str, Any]:
        
        basic_filter = convert_to_basic_filter(content_type=content_type)
        result, remark = await self.repo.get_all_apps_history(order_by, keyword, order_type, limit, offset, basic_filter)
        if len(result) > 0 :
            dresult = []
            for res in result:
                result1, remark1 = await self.repo.get_users_by_user_id(res.user_id)
                if result1:
                    ModUser = ModelUserPartial(
                        firstname=result1.EntityUser.firstname,
                        lastname=result1.EntityUser.lastname,
                        email=result1.EntityUser.email,
                        phone=result1.EntityUser.phone,
                        company=result1.EntityUser.company,
                        address=result1.EntityUser.address,
                        avatar=result1.EntityUser.avatar,
                    )
                    model_apps_history_with_user = ModelAppsHistoryWithUser(
                        user=ModUser,
                        content=res.content,
                        content_type=res.content_type,
                        description=res.description,
                        status=res.status,
                        approved_at=res.approved_at.strftime('%Y-%m-%d %H:%M:%S'),
                        approved_by=res.approved_by,
                        isactive=res.isactive,
                        created_at=res.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    )
                    dresult.append(model_apps_history_with_user)
                else:
                    model_apps_history_with_user = ModelAppsHistoryWithUser(
                        user=None,
                        content=res.content,
                        content_type=res.content_type,
                        description=res.description,
                        status=res.status,
                        approved_at=res.approved_at.strftime('%Y-%m-%d %H:%M:%S'),
                        approved_by=res.approved_by,
                        isactive=res.isactive,
                        created_at=res.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    )
                    dresult.append(model_apps_history_with_user)
                
            return {"status": "00", "remark": remark1, "data": dresult}
        else:
            return {"status": "00", "remark": remark, "data": None}              
        
#SSO ManageResource
    async def new_managed_resource_keycloak(self, type, name: str, rekening:list, max: str, scopes, uris: Array, token: str) -> Dict[str, Any]:        
        url=f"{SERVICE_KEYCLOAK_URL}/realms/openapi/authz/protection/resource_set"
        
        headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                }

        request = {
            "name": name,
            "type": type,
            "icon_uri": "",
            "ownerManagedAccess": True,
            "attributes": {
                "srcRekening": rekening,
                "max": max
            },
            "resource_scopes": scopes,
            "uris": uris
        }
        self.logger.info("new_managed_resource_keycloak", response=request)
        async with self.client.post(url, json=request, headers=headers) as resp:
            response = await resp.text()
            self.logger.info("Keycloak: create manage_reources response", response=request)

            if resp.status==200:
                msgid='00'
                remark='Success'
                return {"status": msgid, "remark": remark, "data": None}
            else:
                msgid=resp.status
                remark='Failed to Fetch data'
                return {"status": msgid, "remark": remark, "data": None}                            

    async def update_rekening_to_keycloak(self, id, name: str, rekening:str, max_rate: str, token: str) -> Dict[str, Any]:        
        url=f"{SERVICE_KEYCLOAK_URL}/realms/openapi/authz/protection/resource_set/" + id
        
        headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                }

        request = {
            "name": name,
            "attributes": {
                "srcRekening": rekening,
                "max": max_rate
            }
        }
        self.logger.info("update_rekening_to_keycloak", response=request)
        async with self.client.put(url, json=request, headers=headers) as resp:
            response = await resp.text()
            self.logger.info("Keycloak: update rekening manage_reources response", response=request)

            if resp.status==204:
                msgid='00'
                remark='Success'
                return {"status": msgid, "remark": remark, "data": None}
            else:
                msgid=resp.status
                remark='Failed to Fetch data'
                return {"status": msgid, "remark": remark, "data": None}                            

    async def get_id_resource_keycloak(self, name: str, token: str) -> Dict[str, Any]:        
        url=f"{SERVICE_KEYCLOAK_URL}/realms/openapi/authz/protection/resource_set?name=" + name
        headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                }

        self.logger.info("get_id_managed_resource_keycloak")
        async with self.client.get(url, headers=headers) as resp:
            response = await resp.text()
            self.logger.info("Keycloak: get id manage_reources response")

            if resp.status==200:
                msgid='00'
                remark='Success'
                return {"status": msgid, "remark": remark, "data": response}
            else:
                msgid=resp.status
                remark='Failed to Fetch data'
                return {"status": msgid, "remark": remark, "data": None}                            

        
    async def delete_managed_resource_keycloak(self, db_id: str, token: str) -> Dict[str, Any]:        
        url=f"{SERVICE_KEYCLOAK_URL}/realms/openapi/authz/protection/resource_set/{id}"
        headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                }

        request = {
        }

        try:
            async with self.client.delete(url, headers=headers) as resp:
                response = await resp.json()
                self.logger.info("Keycloak: delete manage_reources response", response=response)

                if resp.status==200:
                    msgid='00'
                    remark='Success'
                    return {"status": msgid, "remark": remark, "data": None}
                else:
                    msgid=resp.status
                    remark='Failed to Fetch data'
                    return {"status": msgid, "remark": remark, "data": None}                            

        except asyncio.TimeoutError:
            remark = "Request to keycloak service timeout"
            self.logger.warn(remark, url=url, method="POST", body=request)
            result = {"status": "02", "remark": remark, "data": None}
            return result
        except Exception as e:
            remark = "Request to keycloak service error"
            self.logger.error(remark, error=f"{repr(e)} | {str(e)}")
            result = {"status": "02", "remark": remark, "data": None}
            return result
            
    
    async def login_keycloak(self, request: ModelLogin) -> Dict[str, Any]: 
        url=f"{SERVICE_KEYCLOAK_URL}/realms/openapi/protocol/openid-connect/token"
        headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                }
        data = aiohttp.FormData()
        data.add_field('client_id',SERVICE_KEYCLOAK_CLIENTID)
        data.add_field('client_secret',SERVICE_KEYCLOAK_CLIENTSECRET)
        data.add_field('grant_type','password')
        data.add_field('username',request.username)
        data.add_field('password',request.password)

        try:
            async with self.client.post(url, data=data, headers=headers) as resp:
                response = await resp.json()
                #self.logger.info("Keycloak: login response", response=response)
                if resp.status==200:
                    return {"status": "00", "remark": "Success", "data": response}
                else:
                    msgid='02'
                    remark='Failed to Fetch token'
                    return {"status": msgid, "remark": remark, "data": None}
        except asyncio.TimeoutError:
            remark = "Request to keycloak: get token service timeout"
            self.logger.warn(remark, url=url, method="POST", body=request)
            result = {"status": "02", "remark": remark, "data": None}
            return result
        except Exception as e:
            remark = "Request to keycloak: get token service error"
            self.logger.error(remark, error=f"{repr(e)} | {str(e)}")
            result = {"status": "02", "remark": remark, "data": None}
            return result

    async def refresh_token_keycloak(self, request: ModelRefreshToken) -> Dict[str, Any]: 
        url=f"{SERVICE_KEYCLOAK_URL}/realms/openapi/protocol/openid-connect/token"
        headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                }
        data = aiohttp.FormData()
        data.add_field('client_id',SERVICE_KEYCLOAK_CLIENTID)
        data.add_field('client_secret',SERVICE_KEYCLOAK_CLIENTSECRET)
        data.add_field('grant_type','refresh_token')
        data.add_field('refresh_token',request.refresh_token)

        try:
            async with self.client.post(url, data=data, headers=headers) as resp:
                response = await resp.json()
                self.logger.info("Keycloak: refresh token response", response=response)
                if resp.status==200:
                    return {"status": "00", "remark": "Success", "data": response}
                else:
                    msgid='02'
                    remark='Failed to Refresh token'
                    return {"status": msgid, "remark": remark, "data": None}
        except asyncio.TimeoutError:
            remark = "Request to keycloak: get refresh token service timeout"
            self.logger.warn(remark, url=url, method="POST", body=request)
            result = {"status": "02", "remark": remark, "data": None}
            return result
        except Exception as e:
            remark = "Request to keycloak: get refresh token service error"
            self.logger.error(remark, error=f"{repr(e)} | {str(e)}")
            result = {"status": "02", "remark": remark, "data": None}
            return result

#Approved Rekening ManageResource
    async def update_rekening_to_db(self, ckey, max_rate,rekening: str) -> Dict[str, Any]:
        result, msgid, remark = await self.repo.enable_apps_by_ckey(ckey, max_rate, rekening)
        self.logger.info("uremark: " + remark)
        if result:
            return {"status": "00", "remark": remark, "data": result} 
        else:
            return {"status": "02", "remark": remark, "data": None}

    async def approved_rekening_to_keycloak(self, ckey, csecret, name, rekening:str, max_rate: str) -> Dict[str, Any]:        
        dresult4 = await self.login_keycloak_with_client_credentials(ckey, csecret)
        if dresult4['status']=='00':
            result = await self.get_id_resource_keycloak(name, dresult4['data']['access_token'])
            self.logger.info("id resourceset: " + json.dumps(result))
            if result['status'] != '00':
                return {"status": "02", "remark": "Failed to fetch id client_id", "data": None}
            else:
                if len(result) > 0:
                    self.logger.info("get_client_id_keycloak result: " + result['data'][0])
                    id = json.loads(result['data'])[0]
                    result2 = await self.update_rekening_to_keycloak(id, name, rekening, max_rate, dresult4['data']['access_token'])
                    if result2['status'] != '00':
                        msgid='02'
                        remark='Failed to update rekening to keycloak'
                        return {"status": msgid, "remark": remark, "data": None}
                    else:
                        result3 = await self.update_rekening_to_db(ckey, max_rate, rekening)
                        if result3['status'] != '00':
                            msgid='02'
                            remark='Failed to update rekening to db'
                            return {"status": msgid, "remark": remark, "data": None}
                        else:
                            msgid='00'
                            remark='Success'
                            return {"status": msgid, "remark": remark, "data": None} 
                else:
                    msgid='02'
                    remark='Empty resource set'
                    return {"status": msgid, "remark": remark, "data": None}
        else:
            return {"status": '02', "remark": 'Failed to login Credentials', "data": None}
