from app.operated_database.embed.embed_operate import EmbeddingOperatiion
from app.operated_database.qdrant.metric_qdrant_operate import QdrantMetricOperation
from app.operated_database.qdrant.column_qdrant_operate import QdrantColumnOperation
from app.operated_database.es.es_operate import ESOperation
from app.operated_database.mysql.datarepo.mysql_datarepo_operate import DataRepoMySQLOperation
from app.operated_database.mysql.meta.mysql_meta_operate import MetaMySQLOperation
from base_config.meta_data.meta_config import meta_config

from qa_process.agent.LangGraph_context.context_schema import ProcessContext

from qa_process.agent.LangGraph_graph.graph import graph_process

from base_config.log.logger import logger
import json


class QueryService:

    def __init__(self,
        meta_mysql_operate: MetaMySQLOperation,
        datarepo_mysql_operate: DataRepoMySQLOperation,
        es_operate: ESOperation,
        column_qdrant_operate: QdrantColumnOperation,
        metric_qdrant_operate: QdrantMetricOperation,
        embed_operate: EmbeddingOperatiion,
    ):
        self.meta_mysql_operate=meta_mysql_operate
        self.datarepo_mysql_operate=datarepo_mysql_operate
        self.es_operate=es_operate
        self.column_qdrant_operate=column_qdrant_operate
        self.metric_qdrant_operate=metric_qdrant_operate
        self.embed_operate=embed_operate

    async def query(self,query:str):

            logger.info("问答系统初始化...")

            context = ProcessContext(
                meta_mysql_operate=self.meta_mysql_operate,
                datarepo_mysql_operate=self.datarepo_mysql_operate,
                es_operate=self.es_operate,
                column_qdrant_operate=self.column_qdrant_operate,
                metric_qdrant_operate=self.metric_qdrant_operate,
                embed_operate=self.embed_operate,
            )

            graph = await graph_process()

            try:
                async for chunk in graph.astream({"query":query},context=context,stream_mode="custom"):
                    yield f"data:{json.dumps(chunk,ensure_ascii=False,default=str)}\n\n"
            except Exception as e:
                error = {"type":"error","detail":str(e)}
                yield f"data:{json.dumps(error,ensure_ascii=False,default=str)}\n\n"



if __name__ == "__main__":
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
    from base_config.meta_data.meta_config import meta_config

    import asyncio

    meta_mysql_client_management.init()
    meta_mysql_client_management.sync_init()
    dr_mysql_client_management.init()
    dr_mysql_client_management.sync_init()
    es_client_management.init()
    embedding_client_management.init()
    qdrant_client_management.init()

    async def main(query):
        async with(
                meta_mysql_client_management.session_factory() as meta_session,
                dr_mysql_client_management.session_factory() as dr_session,
        ):
            with dr_mysql_client_management.sync_session() as dr_sync_session:

                meta_mysql_operate = MetaMySQLOperation(meta_session,meta_mysql_client_management.sync_engine,meta_config)
                datarepo_mysql_operate = DataRepoMySQLOperation(dr_session,dr_mysql_client_management.sync_engine,dr_sync_session,meta_config)
                es_operate = ESOperation(es_client_management.client)
                column_qdrant_operate = QdrantColumnOperation(qdrant_client_management.client)
                metric_qdrant_operate = QdrantMetricOperation(qdrant_client_management.client)
                embed_operate = EmbeddingOperatiion(embedding_client_management.client)

                q = QueryService(
                    meta_mysql_operate= meta_mysql_operate,
                    datarepo_mysql_operate = datarepo_mysql_operate,
                    es_operate = es_operate,
                    column_qdrant_operate = column_qdrant_operate,
                    metric_qdrant_operate = metric_qdrant_operate,
                    embed_operate = embed_operate
                )

                async for chunk in q.query(query):
                    print(chunk)


    asyncio.run(main("2025年华南地区销售总额"))













