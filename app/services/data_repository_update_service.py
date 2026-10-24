from base_config.log.logger import logger

from base_config.data_repo.datarepo_to_model import FactOrder
from base_config.data_repo.datarepo_to_model import DimCustomer
from base_config.data_repo.datarepo_to_model import DimRegion
from base_config.data_repo.datarepo_to_model import DimProduct
from base_config.data_repo.datarepo_to_model import DimDate

from base_config.data_repo.datarepo_from_config import DataRepository

from app.operated_database.mysql.datarepo.mysql_datarepo_operate import DataRepoMySQLOperation


class DataRepositoryUpdate:

    def __init__(self,
                 data_config:DataRepository,
                 datarepo_mysql_operate:DataRepoMySQLOperation,
                 ):
        self.datarepo_mysql_operate = datarepo_mysql_operate
        self.data_config = data_config

    def confirm_db_tables(self):
        logger.info(f"数仓数据更新前检查数据库表是否完整")
        result = self.datarepo_mysql_operate.confirm_datarepo_db_tables()
        logger.info(f"数仓检查完成")
        return result



    def get_fact_order_values_from_config(self):
        order_ids = [order_id for order_id in self.data_config.fact_order.order_id]
        customer_ids = [customer_id for customer_id in self.data_config.fact_order.customer_id]
        product_ids = [product_id for product_id in self.data_config.fact_order.product_id]
        date_ids = [date_id for date_id in self.data_config.fact_order.date_id]
        region_ids = [region_id for region_id in self.data_config.fact_order.region_id]
        order_quantities = [quantity for quantity in self.data_config.fact_order.order_quantity]
        order_amounts = [amount for amount in self.data_config.fact_order.order_amount]

        return [FactOrder(
            order_id=order_ids[i],
            customer_id=customer_ids[i],
            product_id=product_ids[i],
            date_id=date_ids[i],
            region_id=region_ids[i],
            order_quantity=order_quantities[i],
            order_amount=order_amounts[i]
            ) for i in range(len(product_ids))]


    def get_dim_product_values_from_config(self):
        product_ids = [product for product in self.data_config.dim_product.product_id]
        product_names = [p_n for p_n in self.data_config.dim_product.product_name]
        categorys = [cy for cy in self.data_config.dim_product.category]
        brands = [bd for bd in self.data_config.dim_product.brand]

        return [DimProduct(
            product_id=product_ids[i],
            product_name=product_names[i],
            category=categorys[i],
            brand=brands[i],
        ) for i in range(len(product_ids))]



    def get_dim_region_values_from_config(self):
        region_ids = [reg for reg in self.data_config.dim_region.region_id]
        provinces = [pr for pr in self.data_config.dim_region.province]
        region_names = [reg_n for reg_n in self.data_config.dim_region.region_name]
        countries = [co for co in self.data_config.dim_region.country]

        return [DimRegion(
            region_id=region_ids[i],
            province=provinces[i],
            region_name=region_names[i],
            country=countries[i],
        ) for i in range(len(region_ids))]


    def get_dim_customer_values_from_config(self):
        customer_ids = [ci for ci in self.data_config.dim_customer.customer_id]
        customer_names = [cn for cn in self.data_config.dim_customer.customer_name]
        genders = [ge for ge in self.data_config.dim_customer.gender]
        member_levels = [ml for ml in self.data_config.dim_customer.member_level]

        return [DimCustomer(
            customer_id=customer_ids[i],
            customer_name=customer_names[i],
            gender=genders[i],
            member_level=member_levels[i],
        ) for i in range(len(customer_ids))]


    def get_dim_date_values_from_config(self):
        date_ids = [di for di in self.data_config.dim_date.date_id]
        years = [ye for ye in self.data_config.dim_date.year]
        quarters = [qu for qu in self.data_config.dim_date.quarter]
        months = [mo for mo in self.data_config.dim_date.month]
        days = [day for day in self.data_config.dim_date.day]

        return [DimDate(
            date_id=date_ids[i],
            year=years[i],
            quarter=quarters[i],
            month=months[i],
            day=days[i],
        ) for i in range(len(date_ids))]



    def update(self):
        try:
            result = self.confirm_db_tables()
            if result:
                logger.info(f"数仓数据库表检查完成")
                logger.info(f"数仓数据服务器正在加载配置...")
                dim_customer = self.get_dim_customer_values_from_config()
                dim_region = self.get_dim_region_values_from_config()
                dim_product = self.get_dim_product_values_from_config()
                dim_date = self.get_dim_date_values_from_config()
                fact_order = self.get_fact_order_values_from_config()
                logger.info(f"数仓数据库配置文件已加载完毕...")

                logger.info(f"数仓数据服务器开始更新表数据")
                with self.datarepo_mysql_operate.sync_session.begin():
                    self.datarepo_mysql_operate.update_columns_values_to_dim_customer_table(dim_customer)
                    self.datarepo_mysql_operate.update_columns_values_to_dim_region_table(dim_region)
                    self.datarepo_mysql_operate.update_columns_values_to_dim_product_table(dim_product)
                    self.datarepo_mysql_operate.update_columns_values_to_dim_date_table(dim_date)
                    self.datarepo_mysql_operate.update_columns_values_to_fact_order_table(fact_order)
                self.datarepo_mysql_operate.sync_session.close()
                logger.info(f"数仓数据服务器更新表数据完毕")
            else:
                logger.info(f"数仓数据库表不完整，请检查datarepo数据库表内容...")
                return
        except Exception as e:
            logger.error(f"数仓服务器更新表数据异常:{e}")

