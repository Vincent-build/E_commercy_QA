from typing import TypedDict
from app.operated_database.mysql.meta.mysql_meta_operate import MetaMySQLOperation
from app.operated_database.mysql.datarepo.mysql_datarepo_operate import DataRepoMySQLOperation
from app.operated_database.es.es_operate import ESOperation
from app.operated_database.qdrant.column_qdrant_operate import QdrantColumnOperation
from app.operated_database.qdrant.metric_qdrant_operate import QdrantMetricOperation
from app.operated_database.embed.embed_operate import EmbeddingOperatiion


class ProcessContext(TypedDict):
    meta_mysql_operate:MetaMySQLOperation
    datarepo_mysql_operate:DataRepoMySQLOperation
    es_operate:ESOperation
    column_qdrant_operate:QdrantColumnOperation
    metric_qdrant_operate:QdrantMetricOperation
    embed_operate:EmbeddingOperatiion







