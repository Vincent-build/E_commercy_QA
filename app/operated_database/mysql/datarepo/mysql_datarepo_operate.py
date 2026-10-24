"""
sqlalchemy
创建表
取出数仓表字段的类型、值和信息
校验生成的SQL
执行生成的SQL
"""
from base_config.data_repo.datarepo_to_model import FactOrder
from base_config.data_repo.datarepo_to_model import DimProduct
from base_config.data_repo.datarepo_to_model import DimRegion
from base_config.data_repo.datarepo_to_model import DimCustomer
from base_config.data_repo.datarepo_to_model import DimDate

from app.operated_database.mysql.orm.datarepo_transform_tool.fact_order_trans import FactOrderTransform
from app.operated_database.mysql.orm.datarepo_transform_tool.dim_customer_trans import DimCustomerTransform
from app.operated_database.mysql.orm.datarepo_transform_tool.dim_product_trans import DimProductTransform
from app.operated_database.mysql.orm.datarepo_transform_tool.dim_region_trans import DimRegionTransform
from app.operated_database.mysql.orm.datarepo_transform_tool.dim_date_trans import DimDateTransform

from app.operated_database.mysql.orm.datarepo_db_model.base_model import Base
from base_config.meta_data.meta_config import MetaConfig
from base_config.config.app_config import config as conf
from base_config.log.logger import logger
from sqlalchemy import text,inspect
import asyncio


class DataRepoMySQLOperation:
    def __init__(self,session,sync_engine,sync_session,meta_config:MetaConfig):
        self.session = session
        self.sync_engine = sync_engine
        self.sync_session = sync_session
        self.database = conf.mysql_dr.database
        self.meta_config = meta_config


    def confirm_datarepo_db_tables(self):
        try:
            with self.sync_engine.connect() as session:
                sql = f"SELECT DATABASE()"
                response = session.execute(text(sql))
                database = response.fetchone()[0]
                if database != self.database:
                    logger.warning(f"datarepo Operate :MySQL正在使用{database}数据库,切换到目标{self.database}数据库")
                    sql = f"USE {self.database}"
                    session.execute(text(sql))
                    logger.info(f"已切换MySQL数据库到{self.database}")
            session.close()

            inspector = inspect(self.sync_engine)
            tables = inspector.get_table_names()
            table_names = [table.name for table in self.meta_config.tables]

            if len(tables) != len(table_names) or not tables:
                logger.warning(f"{self.database}数据库表未建全，开始建表...")
                Base.metadata.create_all(self.sync_engine)
                logger.info(f"{self.database}数据库表检查完成")
                return True
            else:
                logger.info(f"{self.database}数据库表检查完成")
                return True
        except Exception as e:
            logger.error(f"Datarepo operate MySQL服务器{self.database}自检失败:{e}")
            return False


    def update_columns_values_to_fact_order_table(self,fact_orders:list[FactOrder]):
        try:
            if fact_orders:
                self.sync_session.add_all([FactOrderTransform.to_model(fact_order) for fact_order in fact_orders])
                logger.info(f"更新{self.database}的fact_order表数据完成")
            else:
                logger.info(f"未检索到配置文件fact_order表更新数据，中止更新")
        except Exception as e:
            logger.error(f"Datarepo Operate 更新{self.database}的fact_order表数据异常:{e}")


    def update_columns_values_to_dim_product_table(self,dim_products:list[DimProduct]):
        try:
            if dim_products:
                self.sync_session.add_all([DimProductTransform.to_model(dim_product) for dim_product in dim_products])
                logger.info(f"更新{self.database}的dim_product表数据完成")
            else:
                logger.info(f"未检索到配置文件dim_product表更新数据，中止更新")
        except Exception as e:
            logger.error(f"Datarepo Operate 更新{self.database}的dim_product表数据异常:{e}")


    def update_columns_values_to_dim_region_table(self,dim_regions:list[DimRegion]):
        try:
            if dim_regions:
                self.sync_session.add_all([DimRegionTransform.to_model(dim_region) for dim_region in dim_regions])
                logger.info(f"更新{self.database}的dim_region表数据完成")
            else:
                logger.info(f"未检索到配置文件dim_region表更新数据，中止更新")
        except Exception as e:
            logger.error(f"Datarepo Operate 更新{self.database}的dim_region表数据异常:{e}")


    def update_columns_values_to_dim_customer_table(self,dim_customers:list[DimCustomer]):
        try:
            if dim_customers:
                self.sync_session.add_all([DimCustomerTransform.to_model(dim_customer) for dim_customer in dim_customers])
                logger.info(f"更新{self.database}的dim_customer表数据完成")
            else:
                logger.info(f"未检索到配置文件dim_customer表更新数据，中止更新")
        except Exception as e:
            logger.error(f"Datarepo Operate 更新{self.database}的dim_customer表数据异常:{e}")


    def update_columns_values_to_dim_date_table(self,dim_dates:list[DimDate]):
        try:
            if dim_dates:
                self.sync_session.add_all([DimDateTransform.to_model(dim_date) for dim_date in dim_dates])
                logger.info(f"更新{self.database}的dim_date表数据完成")
            else:
                logger.info(f"未检索到配置文件dim_date表更新数据，中止更新")
        except Exception as e:
            logger.error(f"Datarepo Operate 更新{self.database}的dim_date表数据异常:{e}")


    async def get_columns_structed_type(self,table_name):
        try:
            sql = f"SHOW columns FROM {table_name}"
            response = await self.session.execute(text(sql))
            rows = response.mappings().fetchall()
            #rows:{'Field': 'order_id', 'Type': 'varchar(30)', 'Null': 'NO', 'Key': 'PRI', 'Default': None, 'Extra': ''}
            return [{row["Field"]:row["Type"]} for row in rows]
        except Exception as e:
            logger.error(f"Datarepo Operate 获取MySQL表结构字段类型失败:{e}")


    async def get_columns_values(self,table_name,column_name,limit:int=10):
        try:
            sql = f"SELECT distinct {column_name} FROM {table_name} Limit {limit}"
            response = await self.session.execute(text(sql))
            rows = response.fetchall()
            return [row[0] for row in rows]
        except Exception as e:
            logger.error(f"Datarepo Operate 获取MySQL表字段值失败:{e}")


    async def get_db_info(self):
        try:
            sql = "SELECT version()"
            response = await self.session.execute(text(sql))
            version = response.fetchone()[0]

            dialect = self.session.bind.dialect.name
            return {"dialect":dialect,"version":version}
        except Exception as e:
            logger.error(f"Datarepo Operate 获取MySQL版本信息失败:{e}")


    async def validate_sql(self,sql:str):
        try:
            sql = f"explain {sql}"
            response = await self.session.execute(text(sql))
            result = response.fetchall()
            if result:
                return True,None
        except Exception as e:
            logger.error(f"Datarepo Operate 校验生成的SQL语句失败:{e}")
            return False,str(e)


    async def run_sql(self,sql:str):
        try:
            response = await self.session.execute(text(sql))
            rows = response.mappings().fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Datarepo Operate 运行生成的SQL语句失败:{e}")


if __name__ == "__main__":
    async def main():
        from app.client.mysql_client import dr_mysql_client_management
        from base_config.meta_data.meta_config import meta_config
        dr_mysql_client_management.init()
        dr_mysql_client_management.sync_init()
        async with dr_mysql_client_management.session_factory() as async_session:
            with dr_mysql_client_management.sync_session() as sync_session:
                mp = DataRepoMySQLOperation(async_session,dr_mysql_client_management.sync_engine,sync_session,meta_config)
        #result = await mp.get_columns_values("nn","age",10)
        #await session.close()
        #print(result)
                result = await mp.validate_sql("SELECT SUM(fact_order.order_amount) AS `销售总额` FROM fact_order INNER JOIN dim_region ON fact_order.region_id = dim_region.region_id INNER JOIN dim_date ON fact_order.date_id = dim_date.date_id WHERE dim_date.year = 2025 AND dim_region.region_name = '华南';")
                print(result)

    asyncio.run(main())

































