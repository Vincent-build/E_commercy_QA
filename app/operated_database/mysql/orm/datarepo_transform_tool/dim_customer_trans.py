from app.operated_database.mysql.orm.datarepo_db_model.datarepo_model import DimCustomerMySQL
from base_config.data_repo.datarepo_to_model import DimCustomer
from dataclasses import asdict


class DimCustomerTransform:

    @staticmethod
    def to_model(dim_customer: DimCustomer) -> DimCustomerMySQL:
        return DimCustomerMySQL(**asdict(dim_customer))