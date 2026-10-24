from app.database_entity.column_info import ColumnInfo
from app.database_entity.metric_info import MetricInfo
from app.database_entity.column_metric import ColumnMetric
from app.database_entity.table_info import TableInfo

from app.operated_database.mysql.orm.meta_db_model.column_info import ColumnInfoMySQL
from app.operated_database.mysql.orm.meta_db_model.metric_info import MetricInfoMySQL
from app.operated_database.mysql.orm.meta_db_model.table_info import TableInfoMySQL
from app.operated_database.mysql.orm.meta_db_model.column_metric import ColumnMetricMySQL

from app.operated_database.mysql.orm.meta_transform_tool.column_info_transform import ColumnInfoTransform
from app.operated_database.mysql.orm.meta_transform_tool.metric_info_transform import MetricInfoTransform
from app.operated_database.mysql.orm.meta_transform_tool.table_info_transform import TableInfoTransform
from app.operated_database.mysql.orm.meta_transform_tool.column_metric_transform import ColumnMetricTransform

from base_config.log.logger import logger
from sqlalchemy import text,inspect
from base_config.meta_data.meta_config import MetaConfig
from typing import Optional
from app.operated_database.mysql.orm.meta_db_model.base_model import Base
from base_config.config.app_config import config as conf

class MetaMySQLOperation:
    def __init__(self,async_session,sync_engine,meta_config:MetaConfig):
        self.session = async_session
        self.sync_engine = sync_engine
        self.meta_config = meta_config
        self.database = conf.mysql_meta.database


    def confirm_meta_db_tables(self):
        try:
            with self.sync_engine.connect() as session:
                sql = "SELECT DATABASE()"
                response = session.execute(text(sql))
                database = response.fetchone()[0]
                if database != self.database:
                    logger.warning(f"Meta Operate :MySQL正在使用{database}数据库,切换到目标{self.database}数据库")
                    sql = f"USE {self.database}"
                    session.execute(text(sql))
                    logger.info(f"已切换MySQL数据库到{self.database}")
                session.close()

            tables = ['column_info', 'column_metric', 'metric_info', 'table_info']
            inspector = inspect(self.sync_engine)
            table_names = inspector.get_table_names()
            if not table_names or len(tables) != len(table_names):
                logger.warning(f"{self.database}数据库表未建全，开始建表...")
                Base.metadata.create_all(self.sync_engine)
                logger.info(f"{self.database}数据库建表完成")
                logger.info(f"{self.database}数据库表检查完成")
            else:
                logger.info(f"{self.database}数据库表检查完成")
        except Exception as e:
            logger.error(f"Metadata operate MySQL服务器{self.database}自检失败:{e}")


    #to_model
    def save_column_infos(self,column_infos:list[ColumnInfo]):
        try:
            self.session.add_all([ColumnInfoTransform.to_model(column_info) for column_info in column_infos])
        except Exception as e:
            logger.error(f"Metadata operate 存储column_info数据库数据出错:{e}")

    def save_metric_infos(self,metric_infos:list[MetricInfo]):
        try:
            self.session.add_all([MetricInfoTransform.to_model(metric_info) for metric_info in metric_infos])
        except Exception as e:
            logger.error(f"Metadata operate 存储metric_info数据库数据出错:{e}")

    def save_table_infos(self,table_infos:list[TableInfo]):
        try:
            self.session.add_all([TableInfoTransform.to_model(table_info) for table_info in table_infos])
        except Exception as e:
            logger.error(f"Metadata operate 存储Table_info数据库数据出错:{e}")

    def save_column_metrics(self,column_metrics:list[ColumnMetric]):
        try:
            self.session.add_all([ColumnMetricTransform.to_model(column_metric) for column_metric in column_metrics])
        except Exception as e:
            logger.error(f"Metadata operate 存储column_metric数据库数据出错:{e}")

    #to_entity
    async def get_column_info(self,id:str)->ColumnInfo | None:
        try:
            column_info:Optional[ColumnInfoMySQL] = await self.session.get(ColumnInfoMySQL,id)
            if column_info:
                return ColumnInfoTransform.to_entity(column_info)
            else:
                return None
        except Exception as e:
            logger.error(f"Metadata operate 获取Column_info数据库数据出错:{e}")

    async def get_table_info(self,id:str)->TableInfo | None:
        try:
            table_info:Optional[TableInfoMySQL] = await self.session.get(TableInfoMySQL,id)
            if table_info:
                return TableInfoTransform.to_entity(table_info)
            else:
                return None
        except Exception as e:
            logger.error(f"Metadata operate 获取Table_info数据库数据出错:{e}")

    async def get_key_columns(self,table_id:str)->list[ColumnInfo] | None:
        try:
            sql = "select * from column_info where table_id= :table_id and role in ('primary_key','foreign_key')"
            response = await self.session.execute(text(sql),{"table_id":table_id})
            result = response.mappings().fetchall()
            if result:
                return [ColumnInfo(**dict(row)) for row in result]
            else:
                return None
        except Exception as e:
            logger.error(f"Metadata operate 获取Column_info数据库数据出错:{e}")


if __name__ == "__main__":
    import asyncio
    async def main():
        from app.client.mysql_client import meta_mysql_client_management
        from base_config.meta_data.meta_config import meta_config
        meta_mysql_client_management.init()
        meta_mysql_client_management.sync_init()
        session = meta_mysql_client_management.session_factory()

        mp = MetaMySQLOperation(session,meta_mysql_client_management.sync_engine,meta_config)
        #result = await mp.get_columns_values("nn","age",10)
        #await session.close()
        #print(result)

        mp.confirm_meta_db_tables()

    asyncio.run(main())




