from app.client.mysql_client import dr_mysql_client_management
from app.client.mysql_client import meta_mysql_client_management
from app.client.embed_model_client import embedding_client_management
from app.client.elasticsearch_client import es_client_management
from app.client.qdrant_client_ import qdrant_client_management

from app.operated_database.mysql.datarepo.mysql_datarepo_operate import DataRepoMySQLOperation
from app.operated_database.mysql.meta.mysql_meta_operate import MetaMySQLOperation
from app.operated_database.embed.embed_operate import EmbeddingOperatiion
from app.operated_database.qdrant.column_qdrant_operate import QdrantColumnOperation
from app.operated_database.qdrant.metric_qdrant_operate import QdrantMetricOperation
from app.operated_database.es.es_operate import ESOperation

from app.services.meta_knowledge_service import MetaKnowledgeService
from app.services.data_repository_update_service import DataRepositoryUpdate

from base_config.meta_data.meta_config import meta_config
from base_config.data_repo.datarepo_from_config import data_repository_config
from base_config.log.logger import logger

async def build():

    #初始化连接
    dr_mysql_client_management.init()
    dr_mysql_client_management.sync_init()
    meta_mysql_client_management.init()
    meta_mysql_client_management.sync_init()
    embedding_client_management.init()
    es_client_management.init()
    qdrant_client_management.init()


    #初始化session
    async with(
        meta_mysql_client_management.session_factory() as meta_session,
        dr_mysql_client_management.session_factory() as dr_session,
    ):
        with dr_mysql_client_management.sync_session() as dr_sync_session:
            #数据库操作工作
            datarepo_mysql_operate = DataRepoMySQLOperation(dr_session,dr_mysql_client_management.sync_engine,dr_sync_session,meta_config)
            meta_mysql_operate = MetaMySQLOperation(meta_session, meta_mysql_client_management.sync_engine, meta_config)
            embed_operate = EmbeddingOperatiion(embedding_client_management.client)
            qdrant_column_operate = QdrantColumnOperation(qdrant_client_management.client)
            qdrant_metric_operate = QdrantMetricOperation(qdrant_client_management.client)
            es_operate = ESOperation(es_client_management.client)

            # 初始化数仓数据更新服务器
            data_repository_service = DataRepositoryUpdate(
                data_repository_config, datarepo_mysql_operate
            )

            if bool(int(input("是否更新数仓?\n 0：不更新 1:更新"))):
                # 开始检查数仓数据更新
                data_repository_service.update()


            #初始化元数据仓库构建服务器
            meta_service = MetaKnowledgeService(
                meta_config=meta_config,
                meta_mysql_operate=meta_mysql_operate,
                datarepo_mysql_operate=datarepo_mysql_operate,
                column_qdrant_operate=qdrant_column_operate,
                metric_qdrant_operate=qdrant_metric_operate,
                embed_operate=embed_operate,
                es_operate=es_operate,
            )

            #开始构建元数据库
            await meta_service.build()

            logger.info(f"元数据库构建完成")

            await dr_mysql_client_management.close()
            await meta_mysql_client_management.close()
            await embedding_client_management.close()
            await es_client_management.close()
            await qdrant_client_management.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(build())














