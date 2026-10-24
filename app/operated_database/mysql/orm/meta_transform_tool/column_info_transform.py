from app.operated_database.mysql.orm.meta_db_model.column_info import ColumnInfoMySQL
from app.database_entity.column_info import ColumnInfo
from dataclasses import asdict

class ColumnInfoTransform:

    @staticmethod
    def to_entity(column_info:ColumnInfoMySQL)->ColumnInfo:
        return ColumnInfo(
            id=column_info.id,
            name=column_info.name,
            type=column_info.type,
            role=column_info.role,
            examples=column_info.examples,
            description=column_info.description,
            alias=column_info.alias,
            table_id=column_info.table_id
        )

    @staticmethod
    def to_model(column_info:ColumnInfo)->ColumnInfoMySQL:
        return ColumnInfoMySQL(**asdict(column_info))
