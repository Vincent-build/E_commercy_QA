from typing import TypedDict,Annotated
from app.database_entity.column_info import ColumnInfo
from app.database_entity.metric_info import MetricInfo
from app.database_entity.value_info import ValueInfo
from operator import add


class ColumnInfoState(TypedDict):
    name: str
    type: str
    role: str
    examples: list
    description: str
    alias: list[str]


class MetricInfoState(TypedDict):
    name: str
    description: str
    relevant_columns: list[str]
    alias: list[str]


class TableInfoState(TypedDict):
    name: str
    description: str
    role: str
    columns: list[ColumnInfoState]


class DateInfoState(TypedDict):
    date: str
    weekday: str
    quarter: str


class DBInfoState(TypedDict):
    version: str
    dialect: str


class DataAgentState(TypedDict):
    query: str
    keywords: list[str]

    retrieval_column_infos: list[ColumnInfo]
    retrieval_metric_infos: list[MetricInfo]
    retrieval_column_values: list[ValueInfo]

    table_infos: list[TableInfoState]
    metric_infos: list[MetricInfoState]
    date_info: DateInfoState
    db_info: DBInfoState

    sql: str
    error: str

    answer:list[dict]

    retry_time:Annotated[int,add]








