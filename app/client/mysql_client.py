from sqlalchemy.ext.asyncio import AsyncEngine,async_sessionmaker,create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base_config.config.app_config import config as conf
from sqlalchemy import create_engine,text
from typing import Optional
from base_config.log.logger import logger
import asyncio




class MySQLManagement:
    def __init__(self,
                 database: str=None,
                 host=conf.mysql_dr.host,
                 port=conf.mysql_dr.port,
                 user=conf.mysql_dr.user,
                 password=conf.mysql_dr.password,
                 ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.engine: Optional[AsyncEngine] = None
        self.session_factory = None
        self.sync_engine = None
        self.sync_session = None


    def _get_url(self):
        if self.database:
            self._check_database()
            return f"mysql+asyncmy://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?charset=utf8mb4"
        else:
            return f"mysql+asyncmy://{self.user}:{self.password}@{self.host}:{self.port}"


    def _check_database(self):
        try:
            logger.info(f"连接MySQL服务器前校验数据库信息")
            url = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}"
            engine = create_engine(url=url)
            with engine.connect() as session:
                sql = "SHOW DATABASES"
                result = session.execute(text(sql)).fetchall()
                list_database = [data[0] for data in result]
                if self.database not in list_database:
                    sql = f"CREATE DATABASE IF NOT EXISTS {self.database}"
                    session.execute(text(sql))
                    session.commit()
                    sql = "SHOW DATABASES"
                    result = session.execute(text(sql))
                    list_database = [data[0] for data in result]
                    if self.database in list_database:
                        logger.info(f"新建{self.database}")
                    else:
                        logger.info(f"新建{self.database}失败")
                    engine.dispose()
                else:
                    engine.dispose()
                    return
        except Exception as e:
            logger.error(f"mysql_client 校验数据库失败:{e}")


    def init(self):
        try:
            url = self._get_url()
            self.engine = create_async_engine(url=url,pool_size=10)
            self.session_factory = async_sessionmaker(self.engine,autoflush=True,expire_on_commit=False)
            logger.info(f"创建异步步引擎完成")
            logger.info(f"完成初始化MySQL服务器连接 -- {self.database}:目标库")
        except Exception as e:
            logger.error(f"初始化MySQL服务器连接失败:{e}")


    async def close(self):
        await self.session_factory.close()
        await self.engine.dispose()
        logger.info(f"MySQL服务器{self.database}连接关闭")


    def sync_init(self):
        """用于建表，只能使用同步引擎"""
        try:
            url = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?charset=utf8mb4"
            self.sync_engine = create_engine(url)
            self.sync_session = sessionmaker(self.sync_engine,autoflush=True,expire_on_commit=False)
            logger.info(f"创建同步引擎完成")
        except Exception as e:
            logger.error(f"创建同步引擎失败:{e}")


    def sync_close(self):
        self.sync_session.close()
        self.sync_engine.dipose()
        logger.info(f"MySQL服务器{self.database}连接关闭")


dr_mysql_client_management = MySQLManagement(conf.mysql_dr.database)
meta_mysql_client_management = MySQLManagement(conf.mysql_meta.database)

if __name__ == "__main__":
    async def main():
        meta_mysql_client_management.init()
        meta_mysql_client_management.sync_init()

    asyncio.run(main())
















