from array import array
import uuid
from typing import List, Tuple, Union
from datetime import datetime

from sqlalchemy.sql.functions import user, now

import gevent
from sqlalchemy import update, delete, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, subqueryload, joinedload
from structlog.types import FilteringBoundLogger

from entities import (
    Base,
    EntityUser,
    EntityApps,
    EntityProducts,
    EntityProductionRequest,
    EntityAppsHistory,
    EntityBaseCrypto
)
from .migrations import products
from models import (
    ModelUser, 
    ModelApps, 
    ModelProducts,
    ModelProductionRequest,
    ModelAppsHistory,
    ModelBaseCrypto
)

from modules.utils import new_object, update_object, get_object_by_id, get_object_all_by_user_id, get_all_object

class UserappRepository:
    def __init__(self, engine: AsyncEngine, logger: FilteringBoundLogger) -> None:
        self.engine = engine
        self.logger = logger
        self.asyncSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async def initDB(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def resetDB(self):
        print('prepare reset DB')
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def new_users(self, request: ModelUser) -> Tuple[Union[None, EntityUser], str, str]:
        #--
        new_user = EntityUser(
            user_id=request.user_id,
            username=request.username,
            firstname=request.firstname,
            lastname=request.lastname,
            email=request.email,
            phone=request.phone,
            company=request.company,
            address=request.address,
            avatar=request.avatar,
            rolecode=request.rolecode,
            isactive=request.isactive,
        )
        return await new_object(self, new_user, request)

    async def update_users(self, request: ModelUser, db_id: str = None) -> Tuple[Union[None, EntityUser], str, str]:
        """
        Update record
        @rtype: object
        """
        query_stmt = select(EntityUser).where(
            EntityUser.db_id == db_id
        )

        update_query_users = (
            update(EntityUser)
                .where(EntityUser.db_id == db_id)
                .values(
                    user_id=request.user_id,
                    username=request.username,
                    firstname=request.firstname,
                    lastname=request.lastname,
                    email=request.email,
                    phone=request.phone,
                    company=request.company,
                    address=request.address,
                    avatar=request.avatar,
                    rolecode=request.rolecode,
                    isactive=request.isactive,
            )
        )

        return await update_object(self, query_stmt, update_query_users, request)

    async def update_users_by_username(self, request: ModelUser) -> Tuple[Union[None, EntityUser], str, str]:
        """
        Update record
        @rtype: object
        """
        query_stmt = select(EntityUser).where(
            EntityUser.username == request.username
        )

        update_query_users = (
            update(EntityUser)
                .where(EntityUser.username == request.username)
                .values(
                    user_id=request.user_id,
                    username=request.username,
                    firstname=request.firstname,
                    lastname=request.lastname,
                    email=request.email,
                    phone=request.phone,
                    company=request.company,
                    address=request.address,
                    avatar=request.avatar,
                    rolecode=request.rolecode,
                    isactive=request.isactive,
            )
        )

        return await update_object(self, query_stmt, update_query_users, request)

    async def check_userapp(self, username: str) -> Tuple[Union[None, EntityUser], str]:
        query_stmt = select(EntityUser).where(
            EntityUser.username == username
        )
        return await get_object_by_id(self, query_stmt, f'username:{username}')

    async def get_users_by_user_id(self, userid: str) -> Tuple[Union[None, EntityUser], str]:
        query_stmt = select(EntityUser).where(
            EntityUser.user_id == userid
        )
        return await get_object_by_id(self, query_stmt, f'user_id:{userid}')
        
    async def get_users_by_db_id(self, db_id: str) -> Tuple[Union[None, EntityUser], str]:
        query_stmt = select(EntityUser).where(
            EntityUser.db_id == db_id
        )
        return await get_object_by_id(self, query_stmt, db_id)

    async def get_all_profile(self, 
        order_by: str, keyword: str, order_type: str,
        limit: int, offset, basic_filter: str='') -> Tuple[List[EntityUser], str]:
        """
        Get all users
        @rtype: ResponseOutCustom
        """
        return await get_all_object(self, 'users', 
            ['username', 'fullname', 'email', 'phone', 'company', 'address', 'company', 'address', 'avatar', 'rolecode'], 'db_id',
            order_by, keyword, order_type, limit, offset, basic_filter)
    
    async def get_all_users_by_rolecode(self, 
        rolecode: str,
        order_by: str, keyword: str, order_type: str,
        limit: int, offset) -> Tuple[List[EntityUser], str]:
        """
        Get all users by type
        @rtype: ResponseOutCustom
        """
        filter = f"rolecode = '{rolecode}'"
        return await get_all_object(self, 'users', 
            ['username', 'firstname', 'lastname', 'email', 'phone', 'company', 'address'], 'db_id',
            order_by, keyword, order_type, limit, offset, filter)

    async def delete_user_by_id(self, db_id: str = None) -> Tuple[Union[None, EntityUser], str, str]:
        """
        Update record
        @rtype: object
        """
        query_stmt = select(EntityUser).where(
            EntityUser.db_id == db_id
        )

        delete_query_user = (
            update(EntityUser)
                .where(EntityUser.db_id == db_id)
                .values(
                    isactive=False,
            )
        )

        return await update_object(self, query_stmt, delete_query_user, '')

    async def delete_user_by_userid(self, user_id: str = None) -> Tuple[Union[None, EntityUser], str, str]:
        """
        Update record
        @rtype: object
        """
        query_stmt = select(EntityUser).where(
            EntityUser.user_id == user_id
        )

        delete_query_user = (
            update(EntityUser)
                .where(EntityUser.user_id == user_id)
                .values(
                    isactive=False,
            )
        )

        return await update_object(self, query_stmt, delete_query_user, '')

    async def check_usercrypto(self, userid: str) -> Tuple[Union[None, EntityBaseCrypto], str]:
        query_stmt = select(EntityBaseCrypto).where(
            EntityBaseCrypto.user_id == userid
        )
        return await get_object_by_id(self, query_stmt, f'user_id:{userid}')

    async def check_apps_by_consumer_secret(self, consumer_secret: str) -> Tuple[Union[None, EntityApps], str]:
        apps_query_stmt = select(EntityApps).where(
            EntityApps.consumer_secret == consumer_secret
        )
        
        return await get_object_by_id(self, apps_query_stmt, f'consumer_secret:{consumer_secret}')

    async def check_apps_by_consumer_key(self, consumer_key: str) -> Tuple[Union[None, EntityApps], str]:
        apps_query_stmt = select(EntityApps).where(
            EntityApps.consumer_key == consumer_key
        )
        
        return await get_object_by_id(self, apps_query_stmt, f'consumer_key:{consumer_key}')

    async def new_usercrypto(self, request: ModelBaseCrypto) -> Tuple[Union[None, EntityBaseCrypto], str, str]:
        #--
        new_usercrypto = EntityBaseCrypto(
            user_id=request.user_id,
            public_key=request.public_key,
            private_key=request.private_key,
            expired_at=request.expired_at,
            isactive=request.isactive
        )
        return await new_object(self, new_usercrypto, request)

    async def get_all_usercrypto(self, 
        order_by: str, keyword: str, order_type: str,
        limit: int, offset, basic_filter: str='') -> Tuple[List[EntityBaseCrypto], str]:
        """
        Get all users
        @rtype: ResponseOutCustom
        """
        return await get_all_object(self, 'basecrypto', 
            ['user_id', 'public_key', 'private_key', 'expired_at', 'isactive'], 'db_id',
            order_by, keyword, order_type, limit, offset, basic_filter)

    async def new_apps(self, request: ModelApps) -> Tuple[Union[None, EntityApps], str, str]:
        #--
        new_apps = EntityApps(
            user_id=request.user_id,
            name=request.name,
            consumer_key=request.consumer_key,
            type=request.type,
            isactive=request.isactive,
            src_accounts=request.src_accounts,
            max_rate=request.max_rate,
            products=request.products
        )
        return await new_object(self, new_apps, request)

    async def check_apps(self, name: str) -> Tuple[Union[None, EntityApps], str]:
        query_stmt = select(EntityApps).where(
            EntityApps.name == name
        )
        return await get_object_by_id(self, query_stmt, f'name:{name}')

    async def update_apps_secret(self, secret: str, consumer_key: str) -> Tuple[Union[None, EntityApps], str, str]:
        """
        Update record
        @rtype: object
        """
        query_stmt = select(EntityApps).where(
            EntityApps.consumer_key == consumer_key
        )

        update_query_apps_secret = (
            update(EntityApps)
                .where(EntityApps.consumer_key == consumer_key)
                .values(
                    consumer_secret=secret,
            )
        )

        return await update_object(self, query_stmt, update_query_apps_secret, '')

    async def delete_apps_by_id(self, db_id: str = None) -> Tuple[Union[None, EntityApps], str, str]:
        """
        Update record
        @rtype: object
        """
        query_stmt = select(EntityApps).where(
            EntityApps.db_id == db_id
        )

        delete_query_apps = (
            update(EntityApps)
                .where(EntityApps.db_id == db_id)
                .values(
                    isactive=False,
            )
        )

        return await update_object(self, query_stmt, delete_query_apps, '')

    async def enable_apps_by_id(self, db_id, max_rate, rekening: str = None) -> Tuple[Union[None, EntityApps], str, str]:
        """
        Update record
        @rtype: object
        """
        rek=[]
        query_stmt = select(EntityApps).where(
            EntityApps.db_id == db_id
        )

        enable_query_apps = (
            update(EntityApps)
                .where(EntityApps.db_id == db_id)
                .values(
                    isactive=True,
                    src_accounts=rek.append(rekening),
                    max_rate=max_rate
            )
        )

        return await update_object(self, query_stmt, enable_query_apps, '')

    async def enable_apps_by_ckey(self, consumer_key, max_rate, rekening: str = None) -> Tuple[Union[None, EntityApps], str, str]:
        """
        Update record
        @rtype: object
        """
        rek=[]
        query_stmt = select(EntityApps).where(
            EntityApps.consumer_key == consumer_key
        )

        enable_query_apps = (
            update(EntityApps)
                .where(EntityApps.consumer_key == consumer_key)
                .values(
                    isactive=True,
                    src_accounts=rek.append(rekening),
                    max_rate=max_rate
            )
        )

        return await update_object(self, query_stmt, enable_query_apps, '')

    async def get_apps_by_userid(self, user_id: str) -> Tuple[List[EntityApps], str]:
        query_stmt = select(EntityApps).where(
            EntityApps.user_id == user_id
        )
        return await get_object_all_by_user_id(self, query_stmt, user_id)
    
    async def get_apps_by_db_id(self, db_id: str) -> Tuple[Union[None, EntityApps], str]:
        query_stmt = select(EntityApps).where(
            EntityApps.db_id == db_id
        )
        return await get_object_by_id(self, query_stmt, db_id)

    async def get_all_apps(self, 
        order_by: str, keyword: str, order_type: str,
        limit: int, offset, basic_filter: str='') -> Tuple[List[EntityApps], str]:
        """
        Get all apps
        @rtype: ResponseOutCustom
        """
        return await get_all_object(self, 'apps', 
            ['db_id', 'name', 'consumer_key', 'consumer_secret', 'type', 'src_accounts','products'], 'db_id',
            order_by, keyword, order_type, limit, offset, basic_filter)

    async def new_products(self, request: ModelProducts) -> Tuple[Union[None, EntityProducts], str, str]:
        #--
        new_products = EntityProducts(
            name=request.name,
            deskripsi=request.deskripsi,
            code=request.code,
            type=request.type,
            isactive=request.isactive,
            uripath=request.uripath,
            method=request.method,
        )
        return await new_object(self, new_products, request)

    async def delete_products_by_id(self, db_id: str = None) -> Tuple[Union[None, EntityProducts], str, str]:
        """
        Update record
        @rtype: object
        """
        query_stmt = select(EntityProducts).where(
            EntityProducts.db_id == db_id
        )

        delete_query_products = (
            update(EntityProducts)
                .where(EntityProducts.db_id == db_id)
                .values(
                    isactive=False,
            )
        )

        return await update_object(self, query_stmt, delete_query_products, '')

    async def get_products_by_db_id(self, db_id: str) -> Tuple[Union[None, EntityProducts], str]:
        query_stmt = select(EntityProducts).where(
            EntityProducts.db_id == db_id
        )
        return await get_object_by_id(self, query_stmt, db_id)

    async def get_all_products(self, 
        order_by: str, keyword: str, order_type: str,
        limit: int, offset, basic_filter: str='') -> Tuple[List[EntityProducts], str]:
        """
        Get all apps
        @rtype: ResponseOutCustom
        """
        return await get_all_object(self, 'products', 
            ['name', 'deskripsi', 'code', 'type', 'uripath', 'method', 'version'], 'db_id',
            order_by, keyword, order_type, limit, offset, basic_filter)

    async def new_production_request(self, request: ModelProductionRequest) -> Tuple[Union[None, EntityProductionRequest], str, str]:
        #--
        new_production_request = EntityProductionRequest(
            user_id=request.user_id,
            requested_by=request.requested_by,
            request_type=request.request_type,
            status=request.status,
            template_file=request.template_file,
            final_file=request.final_file,
            approved_at=datetime.strptime(request.approved_at,'%Y-%m-%d %H:%M:%S'),
            approved_by=request.approved_by,
        )
        return await new_object(self, new_production_request, request)

    async def update_status_production_request(self, status, db_id: str = None) -> Tuple[Union[None, EntityProductionRequest], str, str]:
        """
        Update record
        @rtype: object
        """
        query_stmt = select(EntityProductionRequest).where(
            EntityProductionRequest.db_id == db_id
        )

        update_query_production_request = (
            update(EntityProductionRequest)
                .where(EntityProductionRequest.db_id == db_id)
                .values(
                    status=status,
            )
        )

        return await update_object(self, query_stmt, update_query_production_request, db_id)

    async def update_production_finalfile(self, finalfile, db_id: str = None) -> Tuple[Union[None, EntityProductionRequest], str, str]:
        """
        Update record
        @rtype: object
        """
        query_stmt = select(EntityProductionRequest).where(
            EntityProductionRequest.db_id == db_id
        )

        update_query_production_request = (
            update(EntityProductionRequest)
                .where(EntityProductionRequest.db_id == db_id)
                .values(
                    final_file=finalfile,
            )
        )

        return await update_object(self, query_stmt, update_query_production_request, db_id)

    async def update_production_templatefile(self, templatefile, db_id: str = None) -> Tuple[Union[None, EntityProductionRequest], str, str]:
        """
        Update record
        @rtype: object
        """
        query_stmt = select(EntityProductionRequest).where(
            EntityProductionRequest.db_id == db_id
        )

        update_query_production_request = (
            update(EntityProductionRequest)
                .where(EntityProductionRequest.db_id == db_id)
                .values(
                    template_file=templatefile,
            )
        )

        return await update_object(self, query_stmt, update_query_production_request, db_id)


    async def delete_production_request_by_id(self, db_id: str = None) -> Tuple[Union[None, EntityProductionRequest], str, str]:
        """
        Update record
        @rtype: object
        """
        query_stmt = select(EntityProductionRequest).where(
            EntityProductionRequest.db_id == db_id
        )

        delete_query_production_request = (
            update(EntityProductionRequest)
                .where(EntityProductionRequest.db_id == db_id)
                .values(
                    isactive=False,
            )
        )

        return await update_object(self, query_stmt, delete_query_production_request, '')

    async def get_production_request_by_userid(self, user_id: str) -> Tuple[List[EntityProductionRequest], str]:
        query_stmt = select(EntityProductionRequest).where(
            EntityProductionRequest.user_id == user_id
        )
        return await get_object_all_by_user_id(self, query_stmt, user_id)

    async def get_production_request_by_db_id(self, db_id: str) -> Tuple[Union[None, EntityProductionRequest], str]:
        query_stmt = select(EntityProductionRequest).where(
            EntityProductionRequest.db_id == db_id
        )
        return await get_object_by_id(self, query_stmt, db_id)

    async def get_all_production_request(self, 
        order_by: str, keyword: str, order_type: str,
        limit: int, offset, basic_filter: str='') -> Tuple[List[EntityProductionRequest], str]:
        """
        Get all production_request
        @rtype: ResponseOutCustom
        """
        return await get_all_object(self, 'production_request', 
            ['user_id', 'requested_by', 'request_type', 'status', 'final_file', 'approved_at', 'approved_by'], 'db_id',
            order_by, keyword, order_type, limit, offset, basic_filter)

    async def new_apps_history(self, request: ModelAppsHistory) -> Tuple[Union[None, EntityAppsHistory], str, str]:
        #--
        new_apps_history = EntityAppsHistory(
            user_id=request.user_id,
            content=request.content,
            content_type=request.content_type,
            description=request.description,
            status=request.status,
            approved_at=datetime.strptime(request.approved_at,'%Y-%m-%d %H:%M:%S'),
            approved_by=request.approved_by,
            isactive=request.isactive,
        )
        return await new_object(self, new_apps_history, request)

    async def delete_apps_history_by_id(self, db_id: str = None) -> Tuple[Union[None, EntityAppsHistory], str, str]:
        """
        Update record
        @rtype: object
        """
        query_stmt = select(EntityAppsHistory).where(
            EntityProductionRequest.db_id == db_id
        )

        delete_query_apps_history_request = (
            update(EntityAppsHistory)
                .where(EntityAppsHistory.db_id == db_id)
                .values(
                    isactive=False,
            )
        )

        return await update_object(self, query_stmt, delete_query_apps_history_request, '')

    async def get_apps_history_by_db_id(self, db_id: str) -> Tuple[Union[None, EntityAppsHistory], str]:
        query_stmt = select(EntityAppsHistory).where(
            EntityAppsHistory.db_id == db_id
        )
        return await get_object_by_id(self, query_stmt, db_id)

    async def get_apps_history_by_userid(self, user_id: str) -> Tuple[List[EntityAppsHistory], str]:
        query_stmt = select(EntityAppsHistory).where(
            EntityAppsHistory.user_id == user_id
        )
        return await get_object_all_by_user_id(self, query_stmt, user_id)

    async def get_all_apps_history(self, 
        order_by: str, keyword: str, order_type: str,
        limit: int, offset, basic_filter: str='') -> Tuple[List[EntityAppsHistory], str]:
        """
        Get all production_request
        @rtype: ResponseOutCustom
        """
        return await get_all_object(self, 'app_history', 
            ['user_id', 'content', 'content_type', 'description', 'status', 'approved_at', 'approved_by', 'created_at'], 'db_id',
            order_by, keyword, order_type, limit, offset, basic_filter)
