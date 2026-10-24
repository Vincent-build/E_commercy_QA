from typing import Annotated
from fastapi import Depends
from sqlalchemy import Engine

from base_config.data_repo.datarepo_from_config import data_repository_config,DataRepository

from qa_process.query_service.query_service import QueryService
from app.services.meta_knowledge_service import MetaKnowledgeService
from app.services.data_repository_update_service import DataRepositoryUpdate

from app.client.mysql_client import meta_mysql_client_management
from app.client.mysql_client import dr_mysql_client_management
from app.client.embed_model_client import embedding_client_management
from app.client.qdrant_client_ import qdrant_client_management
from app.client.elasticsearch_client import es_client_management

from app.operated_database.embed.embed_operate import EmbeddingOperatiion
from app.operated_database.qdrant.metric_qdrant_operate import QdrantMetricOperation
from app.operated_database.qdrant.column_qdrant_operate import QdrantColumnOperation
from app.operated_database.es.es_operate import ESOperation
from app.operated_database.mysql.datarepo.mysql_datarepo_operate import DataRepoMySQLOperation
from app.operated_database.mysql.meta.mysql_meta_operate import MetaMySQLOperation
from base_config.meta_data.meta_config import meta_config,MetaConfig

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


async def get_meta_session():
    async with meta_mysql_client_management.session_factory() as meta_session:
        yield meta_session

async def get_meta_sync_engine():
    return meta_mysql_client_management.sync_engine

async def get_meta_config():
    return meta_config

async def get_datarepo_config():
    return data_repository_config

async def get_daterepo_session():
    async with dr_mysql_client_management.session_factory() as datarepo_session:
        yield datarepo_session

async def get_datarepo_sync_session():
    with dr_mysql_client_management.sync_session() as datarepo_sync_session:
        yield datarepo_sync_session

async def get_datarepo_sync_engine():
    return dr_mysql_client_management.sync_engine


async def get_meta_mysql_operator(
        meta_session:Annotated[AsyncSession,Depends(get_meta_session)],
        sync_engine:Annotated[Engine,Depends(get_meta_sync_engine)],
        meta_config_:Annotated[MetaConfig,Depends(get_meta_config)]):
    return MetaMySQLOperation(meta_session,sync_engine,meta_config_)


async def get_datarepo_mysql_operator(
        datarepo_session:Annotated[AsyncSession,Depends(get_daterepo_session)],
        sync_session:Annotated[Session,Depends(get_datarepo_sync_session)],
        sync_engine:Annotated[Engine,Depends(get_datarepo_sync_engine)],
        meta_config_:Annotated[MetaConfig,Depends(get_meta_config)]):
    return DataRepoMySQLOperation(datarepo_session,sync_engine,sync_session, meta_config_)


async def get_metric_qdrant_operator():
    return QdrantMetricOperation(qdrant_client_management.client)


async def get_column_qdrant_operator():
    return QdrantColumnOperation(qdrant_client_management.client)


async def get_es_operator():
    return ESOperation(es_client_management.client)


async def get_embed_operator():
    return EmbeddingOperatiion(embedding_client_management.client)

async def get_query_service(
        meta_mysql_operate: Annotated[MetaMySQLOperation,Depends(get_meta_mysql_operator)],
        datarepo_mysql_operate: Annotated[DataRepoMySQLOperation,Depends(get_datarepo_mysql_operator)],
        es_operate: Annotated[ESOperation,Depends(get_es_operator)],
        column_qdrant_operate: Annotated[QdrantColumnOperation,Depends(get_column_qdrant_operator)],
        metric_qdrant_operate: Annotated[QdrantMetricOperation,Depends(get_metric_qdrant_operator)],
        embed_operate: Annotated[EmbeddingOperatiion,Depends(get_embed_operator)],
):
    return QueryService(
        meta_mysql_operate=meta_mysql_operate,
        datarepo_mysql_operate=datarepo_mysql_operate,
        es_operate=es_operate,
        column_qdrant_operate=column_qdrant_operate,
        metric_qdrant_operate=metric_qdrant_operate,
        embed_operate=embed_operate,
    )



async def get_meta_service(
                datarepo_mysql_operate:Annotated[DataRepoMySQLOperation,Depends(get_datarepo_mysql_operator)],
                meta_mysql_operate:Annotated[MetaMySQLOperation,Depends(get_meta_mysql_operator)],
                metric_qdrant_operate:Annotated[QdrantMetricOperation,Depends(get_metric_qdrant_operator)],
                column_qdrant_operate:Annotated[QdrantColumnOperation,Depends(get_column_qdrant_operator)],
                embed_operate:Annotated[EmbeddingOperatiion,Depends(get_embed_operator)],
                es_operate:Annotated[ESOperation,Depends(get_es_operator)],
                meta_config_:Annotated[MetaConfig,Depends(get_meta_config)],
):
    return MetaKnowledgeService(
        meta_config=meta_config_,
        datarepo_mysql_operate=datarepo_mysql_operate,
        meta_mysql_operate=meta_mysql_operate,
        metric_qdrant_operate=metric_qdrant_operate,
        column_qdrant_operate=column_qdrant_operate,
        embed_operate=embed_operate,
        es_operate=es_operate,
    )


async def update_datarepo_service(
                datarepo_mysql_operate:Annotated[DataRepoMySQLOperation,Depends(get_datarepo_mysql_operator)],
                data_config:Annotated[DataRepository,Depends(get_datarepo_config)],
):
    return DataRepositoryUpdate(
        datarepo_mysql_operate = datarepo_mysql_operate,
        data_config = data_config,
    )














