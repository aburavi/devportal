from datetime import date
from pydantic import BaseModel
from typing import List, Optional

from sqlalchemy.sql.coercions import LimitOffsetImpl

class ModelLogin(BaseModel):
    username : Optional[str]
    password : Optional[str]

class ModelRefreshToken(BaseModel):
    refresh_token : Optional[str]

class ModelUser(BaseModel):
    user_id : Optional[str]
    username : Optional[str]
    password : Optional[str]
    firstname : Optional[str]
    lastname : Optional[str]
    email : Optional[str]
    phone : Optional[str]
    company : Optional[str]
    address : Optional[str]
    rolecode : Optional[str]
    isactive : Optional[bool]
    avatar: Optional[str]

class ModelUserPartial(BaseModel):
    firstname : Optional[str]
    lastname : Optional[str]
    email : Optional[str]
    phone : Optional[str]
    company : Optional[str]
    address : Optional[str]
    avatar: Optional[str]

class ModelApps(BaseModel):
    user_id : Optional[str]
    name : Optional[str]
    consumer_key : Optional[str]
    consumer_secret : Optional[str]
    type : Optional[str]
    src_accounts : Optional[List[str]]
    max_rate: Optional[str]
    products : Optional[List[str]]
    isactive : Optional[bool]

class ModelAppsWithUser(BaseModel):
    user : Optional[ModelUserPartial]
    name : Optional[str]
    consumer_key : Optional[str]
    consumer_secret : Optional[str]
    type : Optional[str]
    src_accounts : Optional[List[str]]
    max_rate: Optional[str]
    products : Optional[List[str]]
    isactive : Optional[bool]

class ModelBaseCrypto(BaseModel):
    user_id : Optional[str]
    public_key : Optional[str]
    private_key : Optional[str]
    expired_at : Optional[date]
    isactive : Optional[bool]

class ModelBaseCryptoWithUser(BaseModel):
    user : Optional[ModelUserPartial]
    public_key : Optional[str]
    private_key : Optional[str]
    expired_at : Optional[date]
    isactive : Optional[bool]

class ModelProducts(BaseModel):
    name : Optional[str]
    deskripsi : Optional[str]
    type : Optional[str]
    code : Optional[str]
    uripath : Optional[str]
    method : Optional[str]
    version : Optional[str]
    isactive : Optional[bool]

class ModelProductionRequest(BaseModel):
    user_id : Optional[str]
    requested_by : Optional[str]
    request_type : Optional[str]
    status : Optional[str]
    template_file : Optional[str]
    final_file: Optional[str]
    approved_at : Optional[str]
    approved_by : Optional[str]
    isactive : Optional[bool]

class ModelProductionRequestWithUser(BaseModel):
    db_id : Optional[str]
    user : Optional[ModelUserPartial]
    requested_by : Optional[str]
    request_type : Optional[str]
    status : Optional[str]
    template_file : Optional[str]
    final_file: Optional[str]
    approved_at : Optional[str]
    approved_by : Optional[str]
    isactive : Optional[bool]

class ModelAppsHistory(BaseModel):
    user_id : Optional[str]
    content : Optional[str]
    content_type : Optional[str]
    description : Optional[str]
    status : Optional[str]
    approved_at : Optional[str]
    approved_by : Optional[str]
    isactive : Optional[bool]

class ModelAppsHistoryWithUser(BaseModel):
    user : Optional[ModelUserPartial]
    content : Optional[str]
    content_type : Optional[str]
    description : Optional[str]
    status : Optional[str]
    approved_at : Optional[str]
    approved_by : Optional[str]
    isactive : Optional[bool]
    created_at: Optional[str]

class ModelApprovedApps(BaseModel):
    consumer_key : Optional[str]
    consumer_secret : Optional[str]
    name : Optional[str]
    src_accounts : Optional[str]
    max_rate : Optional[str]
    isactive : Optional[bool]