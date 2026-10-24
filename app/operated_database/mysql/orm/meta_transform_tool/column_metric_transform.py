from app.operated_database.mysql.orm.meta_db_model.column_metric import ColumnMetricMySQL
from app.database_entity.column_metric import ColumnMetric
from dataclasses import asdict

class ColumnMetricTransform:

    @staticmethod
    def to_entity(column_metric:ColumnMetricMySQL)->ColumnMetric:
        return ColumnMetric(
            column_id=column_metric.column_id,
            metric_id=column_metric.metric_id,
        )

    @staticmethod
    def to_model(column_metric:ColumnMetric)->ColumnMetricMySQL:
        return ColumnMetricMySQL(**asdict(column_metric))