import gevent
from fastapi.logger import logger
from sqlalchemy import insert, select, text
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.ext.asyncio.engine import AsyncEngine
import csv
import os

from entities import EntityProducts

ROOT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)  # This is project Root

SQL_PATH = os.path.join(ROOT_DIR, "repository/sql")

products_dict = [
    {
        "filename": "openapi-products.sql",
        "check_query": select(EntityProducts.code).limit(1),
    }
]

async def products(con: AsyncEngine):
    logger.info("Start Products Seeding...")
    # check data already exist or not
    try:
        for location in products_dict:
            logger.info(f"Seeding {location['filename']}...")
            result = await con.execute(location["check_query"])
            await con.commit()
            count = len(result.scalars().all())
            # check data exists or not
            if count <= 0:
                # execute insert query
                file = open(os.path.join(SQL_PATH, location["filename"]))
                query = text(file.read())
                await con.execute(query)
                await con.commit()
                file.close()
                logger.info(f"Seeding {location['filename']} success...")
            else:
                logger.info("Data already exists, skip seeding...")

    except gevent.Timeout:
        # database timeout
        logger.error("Seeding failed, DB timeout...")

    except SQLAlchemyError as e:
        logger.error(e)
        # rollback db if error
        logger.error("Seeding failed, duplicate rows..." + e)
        await con.rollback()

        #logger.error("Drop table, for recreating")
        #sql = text("DROP TABLE IF EXISTS {}".format("enum_content_data"))
        #await con.execute(sql)
        #await con.commit()

