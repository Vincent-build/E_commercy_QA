from app.operated_database.mysql.orm.meta_db_model.table_info import TableInfoMySQL
from app.database_entity.table_info import TableInfo
from dataclasses import asdict


class TableInfoTransform:

    @staticmethod
    def to_entity(table_info:TableInfoMySQL)->TableInfo:
        return TableInfo(
            id=table_info.id,
            name=table_info.name,
            role=table_info.role,
            description=table_info.description
        )

    @staticmethod
    def to_model(table_info:TableInfo)->TableInfoMySQL:
        return TableInfoMySQL(**asdict(table_info))


