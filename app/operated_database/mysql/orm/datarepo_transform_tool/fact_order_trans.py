from app.operated_database.mysql.orm.datarepo_db_model.datarepo_model import FactOrderMySQL
from base_config.data_repo.datarepo_to_model import FactOrder
from dataclasses import asdict


class FactOrderTransform:

    @staticmethod
    def to_model(fact_order:FactOrder)->FactOrderMySQL:
        return FactOrderMySQL(**asdict(fact_order))