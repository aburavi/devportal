import gevent

from typing import TypeVar, Type, Tuple, Union, List
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from entities import Base
from datetime import datetime, timedelta

EntityType = TypeVar("EntityType", bound=Base)
ModelType = TypeVar("ModelType", bound=BaseModel)

def convert_to_basic_filter(**filters):
    fs = []
    if 'isactive' in filters and filters['isactive']:
        fs.append(f"isactive = {filters['isactive']}")
    for s in ['user_id', 'rolecode', 'type', 'request_type', 'content_type']:
        if s in filters and filters[s]:
            fs.append(f"{s} = '{filters[s]}'")

    print('basic_filter: ' + " and ". join(fs))
    return " and ". join(fs)

async def new_object(repo, new_data: Type[EntityType],
    request: Type[ModelType] = None) -> Tuple[Union[None, Type[EntityType]], str, str]:

    async with repo.asyncSession() as session:
        try:
            # insert as query as buck
            session.add(new_data)
            await session.commit()

            remark = "Success"
            message_id = "00"
            return new_data, message_id, remark

        except gevent.Timeout:
            # database timeout
            repo.logger.warn("Insert data to DB timeout", data=request)
            await session.invalidate()
            remark = "Failed, DB transaction was timed out..."
            message_id = "02"
            return None, message_id, remark

        except SQLAlchemyError as e:
            repo.logger.error("Insert data to DB error", error=str(e), data=request)
            # rollback db if error
            await session.rollback()
            remark = "Failed, DB transaction was failed..."
            message_id = "02"
            return None, message_id, remark

async def update_object(repo, query_stmt, update_query,
    request: Type[ModelType] = None) -> Tuple[Union[None, Type[EntityType]], str, str]:

    async with repo.asyncSession() as session:
        try:
            # PUT : update table from database with query and async session
            # execute query
            proxy_row = await session.execute(query_stmt)

            # parse result as list of object
            result = proxy_row.fetchone()
            await session.commit()
            
            # first check
            if not result:
                remark = f"No query found..."
                message_id = "01"
                return None, message_id, remark

            await session.execute(update_query)
            await session.commit()

            remark = "Success"
            message_id = "00"
            return result, message_id, remark

        except gevent.Timeout:
            # database timeout
            repo.logger.warn("Update data to DB timeout", data=request)
            await session.invalidate()
            remark = "Failed, DB transaction was timed out..."
            message_id = "02"
            return None, message_id, remark

        except SQLAlchemyError as e:
            repo.logger.error("Update data to DB error", error=str(e), data=request)
            # rollback db if error
            await session.rollback()
            remark = "Failed, DB transaction was timed out..."
            message_id = "02"
            return None, message_id, remark

async def get_object_by_id(repo, query_stmt, db_id
    ) -> Tuple[Union[None, Type[EntityType]], str]:

    async with repo.asyncSession() as session:
        try:
            # GET : get spesific from model table from database with query and async session
            proxy_row = await session.execute(query_stmt)
            result = proxy_row.fetchone()
            await session.commit()
            # result data handling
            if result:
                remark = "Success"
                return result, remark
            else:
                # data not found
                remark = f"No query found..."
                return None, remark

        except gevent.Timeout:
            # database timeout
            repo.logger.warn("Query data from DB timeout", db_id=db_id)
            await session.invalidate()
            remark = "Failed, DB query was timed out..."
            return None, remark

        except SQLAlchemyError as e:
            repo.logger.error("Query data from DB error", error=str(e), db_id=db_id)
            # rollback db if error
            await session.rollback()
            remark = "Failed, DB query was failed..."
            return None, remark

async def get_object_all_by_user_id(repo, query_stmt, db_id
    ) -> Tuple[List[Type[EntityType]], str]:

    async with repo.asyncSession() as session:
        try:
            # GET : get spesific from model table from database with query and async session
            proxy_row = await session.execute(query_stmt)
            result = proxy_row.fetchall()
            await session.commit()
            # result data handling
            if result:
                remark = "Success"
                return result, remark
            else:
                # data not found
                remark = f"No query found..."
                return None, remark

        except gevent.Timeout:
            # database timeout
            repo.logger.warn("Query data from DB timeout", user_id=db_id)
            await session.invalidate()
            remark = "Failed, DB query was timed out..."
            return None, remark

        except SQLAlchemyError as e:
            repo.logger.error("Query data from DB error", error=str(e), user_id=db_id)
            # rollback db if error
            await session.rollback()
            remark = "Failed, DB query was failed..."
            return None, remark

async def get_all_object(repo, objectname: str, 
    search_cols: List, default_order_by: str,
    order_by: str, keyword: str, order_type: str,
    limit: int, offset: int, basic_filter: str=''
    ) -> Tuple[List[Type[EntityType]], str]:

    async with repo.asyncSession() as session:
        try:
            if not order_by: order_by = default_order_by
            if keyword is None or keyword == "":
                if basic_filter == '':
                    filter = f'WHERE (isactive = TRUE)'
                else:
                    filter = f'WHERE ({basic_filter})'
            else:
                sfilter = ' or '.join([f"{col} LIKE '%{keyword}%'" for col in search_cols])
                if basic_filter == '':
                    filter = f"WHERE ({sfilter} and isactive = TRUE)"
                else:
                    filter = f'WHERE ({basic_filter} and ({sfilter}))'
            #--
            # create query
            query_stmt = f"""
                SELECT *
                FROM {objectname}
                {filter}
                ORDER BY {order_by} {order_type}
                LIMIT {limit}
                OFFSET {offset};
            """
            # execute query
            proxy_rows = await session.execute(query_stmt)
            # parse result as list of object
            result = proxy_rows.fetchall()

            # commit the db transaction
            await session.commit()

            # return the result as custom response
            remark = "Success"
            return result, remark

        except gevent.Timeout:
            # database timeout
            repo.logger.warn("Query all {objectname} data timeout", limit=limit, offset=offset)
            await session.invalidate()
            remark = "Failed, DB transaction was timed out..."
            return [], remark

        except SQLAlchemyError as e:
            repo.logger.error("Query all {objectname} data DB error", error=str(e))
            # rollback db if error
            await session.rollback()
            remark = "Failed, DB transaction was timed out..."
            return [], remark

async def get_count_object(repo, objectname: str, 
    search_cols: List, default_order_by: str,
    order_by: str, keyword: str, order_type: str,
    basic_filter: str=''
    ) -> Tuple[int, float, str]:

    async with repo.asyncSession() as session:
        try:
            if not order_by: order_by = default_order_by
            if keyword is None or keyword == "":
                if basic_filter == '':
                    filter = ""
                else:
                    filter = f'WHERE ({basic_filter})'
            else:
                sfilter = ' or '.join([f"{col} LIKE '%{keyword}%'" for col in search_cols])
                if basic_filter == '':
                    filter = f"WHERE ({sfilter})"
                else:
                    filter = f'WHERE ({basic_filter} and ({sfilter}))'
            #--
   
            # count query
            count_stmt = f"""
                SELECT count(*)
                FROM {objectname}
                {filter}
            """
            # execute query
            proxy_rows = await session.execute(count_stmt)
            # parse result as list of object
            count = proxy_rows.scalar()
            # commit the db transaction
            await session.commit()

            # create query
            query_stmt = f"""
                SELECT *
                FROM {objectname}
                {filter}
                ORDER BY {order_by} {order_type}
            """
            # execute query
            proxy_rows = await session.execute(query_stmt)
            # parse result as list of object
            result = proxy_rows.fetchall()
            # commit the db transaction
            await session.commit()

            sumrating = 0
            for s in result:
                sumrating = sumrating + s['cust_rating']
            rating = sumrating/count
            # return the result as custom response
            remark = "Success"
            return count, rating, remark

        except gevent.Timeout:
            # database timeout
            repo.logger.warn("Query all {objectname} data timeout", limit=limit, offset=offset)
            await session.invalidate()
            remark = "Failed, DB transaction was timed out..."
            return 0, 0.0, remark

        except SQLAlchemyError as e:
            repo.logger.error("Query all {objectname} data DB error", error=str(e))
            # rollback db if error
            await session.rollback()
            remark = "Failed, DB transaction was timed out..."
            return 0, 0, remark

async def get_object_with_statement(repo, query_stmt) -> Tuple[List[Type[EntityType]], str]:
    async with repo.asyncSession() as session:
        try:
            # GET : get spesific from model table from database with query and async session
            print(query_stmt)
            repo.logger.info('Querying database')
            proxy_row = await session.execute(query_stmt)
            result = proxy_row.fetchall()
            await session.commit()

        except gevent.Timeout:
            # database timeout
            repo.logger.warn("Query data from DB timeout")
            await session.invalidate()
            remark = "Failed, DB query was timed out..."
            return None, remark

        except SQLAlchemyError as e:
            repo.logger.error("Query data from DB error", error=str(e))
            # rollback db if error
            await session.rollback()
            remark = "Failed, DB query was failed..."
            return None, remark

        # result data handling
        if result:
            # get new data
            # return the result as custom response
            print(result)
            remark = "Success"
            return result, remark
        else:
            # data not found
            remark = f"Failed, data with not found..."
            return None, remark