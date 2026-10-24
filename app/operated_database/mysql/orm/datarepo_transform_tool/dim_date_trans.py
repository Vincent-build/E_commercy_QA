from app.operated_database.mysql.orm.datarepo_db_model.datarepo_model import DimDateMySQL
from base_config.data_repo.datarepo_to_model import DimDate
from dataclasses import asdict


class DimDateTransform:

    @staticmethod
    def to_model(dim_date:DimDate) -> DimDateMySQL:
        return DimDateMySQL(**asdict(dim_date))