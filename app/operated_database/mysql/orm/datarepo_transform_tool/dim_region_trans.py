from app.operated_database.mysql.orm.datarepo_db_model.datarepo_model import DimRegionMySQL
from base_config.data_repo.datarepo_to_model import DimRegion
from dataclasses import asdict

class DimRegionTransform:

    @staticmethod
    def to_model(dim_region:DimRegion)->DimRegionMySQL:
        return DimRegionMySQL(**asdict(dim_region))