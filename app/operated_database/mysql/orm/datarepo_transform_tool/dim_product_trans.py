from app.operated_database.mysql.orm.datarepo_db_model.datarepo_model import DimProductMySQL
from base_config.data_repo.datarepo_to_model import DimProduct
from dataclasses import asdict


class DimProductTransform:

    @staticmethod
    def to_model(dim_product: DimProduct) -> DimProductMySQL:
        return DimProductMySQL(**asdict(dim_product))