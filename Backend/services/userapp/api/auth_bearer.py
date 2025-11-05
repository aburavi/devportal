from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Any, Dict, List, Tuple, Union
from datetime import datetime
import logging
import jwt
import os

JWT_PUBKEY = os.getenv("SERVICE_APP_JWT_PUBKEY", 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzOW6WuQoX9X4SFZUqW0p8ZK8KXX54DoZ961KQ9bL9QCqaBjx7CQTUhRVpAIdW98eFGMM3dF7fyZt7douI0YpPFJL4scU6kDZxZ1PeGnk6Uk/PXBQCSVaQGOpWytIfaxzLOYavdXCahzyt/2CkQFEv/uoS6EHTfGlk8pxGtRmTqrtFy3WDGdqXjKfZDPLBYLAvp5JGUjmxLWPaKesrFsMqA5LocMEE+CTq1OeahWPX23el7WhLZ8GBRPpee3gas7ojNzFj1p71ukV3ZkbZ4o6WGU98Auus0XMAvqh8qJuo8GaSjF8WUmWkB23kLY6NIGuEN8y6sxNzqWHgI1VIbJ5aQIDAQAB')

logging.basicConfig(level=logging.DEBUG)

class JWTBearer(HTTPBearer):
    def __init__(self, roles: List = [], auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.roles = roles

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            payload = await self.verify_jwt(credentials.credentials)
            if not payload:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
    
    async def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = jwt.decode(jwtoken, JWT_PUBKEY, algorithms=['RS256'], options={"verify_signature": False})
        except:
            return None

        if not payload or payload['exp'] < int(datetime.now().timestamp()):
            return None
        
        if len(self.roles) > 0 and not payload.get('rolecode', '') in self.roles:
            raise HTTPException(status_code=403, detail="Insufficient rights to access resources")
        
        return payload

    async def verify_token(jwtoken: str, roles: List) -> bool:
        try:
            payload = jwt.decode(jwtoken, JWT_PUBKEY, algorithms=['RS256'], options={"verify_signature": False})
        except:
            raise HTTPException(status_code=403, detail="Invalid token.")

        if not payload or payload['exp'] < int(datetime.now().timestamp()):
            raise HTTPException(status_code=403, detail="Expired token.")
        
        if len(roles) > 0 and not payload.get('rolecode', '') in roles:
            raise HTTPException(status_code=403, detail="Insufficient rights to access resources")
        
        return payload

    async def token_payload(jwtoken: str) -> Tuple[Union[None, Dict], bool]:
        isTokenValid: bool = False
        try:
            dpayload = jwt.decode(jwtoken, JWT_PUBKEY, algorithms=['RS256'], options={"verify_signature": False})
            payload = dict(dpayload)
        except:
            payload = None

        if payload and payload['exp'] >= int(datetime.now().timestamp()):
            isTokenValid = True

        logging.debug(f'isTokenValid: {isTokenValid}')
        return payload, isTokenValid