"""
元数据知识库构建的核心业务框架

存储Column_info数据到Qdrant
存储Value_info数据到ES
存储
"""
from base_config.log.logger import logger

from base_config.meta_data.meta_config import MetaConfig

from app.operated_database.mysql.datarepo.mysql_datarepo_operate import DataRepoMySQLOperation
from app.operated_database.mysql.meta.mysql_meta_operate import MetaMySQLOperation
from app.operated_database.qdrant.column_qdrant_operate import QdrantColumnOperation
from app.operated_database.qdrant.metric_qdrant_operate import QdrantMetricOperation
from app.operated_database.es.es_operate import ESOperation
from app.operated_database.embed.embed_operate import EmbeddingOperatiion

from app.database_entity.column_metric import ColumnMetric
from app.database_entity.metric_info import MetricInfo
from app.database_entity.column_info import ColumnInfo
from app.database_entity.table_info import TableInfo
from app.database_entity.value_info import ValueInfo

from uuid import uuid4
from dataclasses import asdict
from qdrant_client.models import PointStruct




class MetaKnowledgeService:

    def __init__(self,
                 meta_config:MetaConfig,
                 datarepo_mysql_operate:DataRepoMySQLOperation,
                 meta_mysql_operate:MetaMySQLOperation,
                 metric_qdrant_operate:QdrantMetricOperation,
                 column_qdrant_operate:QdrantColumnOperation,
                 embed_operate:EmbeddingOperatiion,
                 es_operate:ESOperation,
                 ):
        self.datarepo_mysql_operate = datarepo_mysql_operate
        self.meta_mysql_operate = meta_mysql_operate
        self.column_qdrant_operate = column_qdrant_operate
        self.metric_qdrant_operate = metric_qdrant_operate
        self.embed_operate = embed_operate
        self.es_operate = es_operate
        self.meta_config = meta_config

    async def _save_tables_to_meta_db(self):
        try:
            table_infos = []
            column_infos = []

            for table in self.meta_config.tables:
                table_info = TableInfo(
                    id=table.name,
                    name=table.name,
                    role=table.role,
                    description=table.description,
                )

                column_type = await self.datarepo_mysql_operate.get_columns_structed_type(table.name)

                table_infos.append(table_info)

                for column in table.columns:

                    examples = await self.datarepo_mysql_operate.get_columns_values(table.name,column.name,1000)

                    type = [types[column.name] for types in column_type if types.get(column.name)][0]

                    column_info = ColumnInfo(
                        id=f"{table.name}.{column.name}",
                        name=column.name,
                        role=column.role,
                        description=column.description,
                        alias=column.alias,
                        type=type,
                        examples=examples,
                        table_id=table.name,
                    )

                    column_infos.append(column_info)

            async with self.meta_mysql_operate.session.begin():
                self.meta_mysql_operate.save_table_infos(table_infos)
                self.meta_mysql_operate.save_column_infos(column_infos)

            return column_infos

        except Exception as e:
            logger.error(f"Meta Service -- MySQL meta数据库存储tables数据失败：{e}")


    async def _save_column_info_to_qdrant(self,column_infos:list[ColumnInfo]):
        """把column_info中的name、description、alias放进去"""
        try:
            await self.column_qdrant_operate.confirm_collection()
            points = []
            for column_info in column_infos:
                elements = []
                embeddings = []
                elements.extend([column_info.name,column_info.description])
                elements.extend([alia for alia in column_info.alias])
                logger.info(f"Qdrant数据{column_info.name}进行批量向量化处理中...")
                for element in elements:
                    embed = await self.embed_operate.embed(element)
                    embeddings.extend(embed)
                points.extend([PointStruct(id=uuid4(),vector=embedding,payload=asdict(column_info)) for embedding in embeddings])
            await self.column_qdrant_operate.upsert(points)
        except Exception as e:
            logger.error(f"Meta Service -- Qdrant 存储columns数据失败:{e}")


    async def _save_value_info_to_es(self,column_infos:list[ColumnInfo]):
        """根据sync是否同步值，把column_info中的值与table_id放进es中"""
        try:
            await self.es_operate.confirm_index()

            judge_sync:dict[str,bool] = {}

            documents = []

            for table in self.meta_config.tables:
                for column in table.columns:
                    judge_sync[f'{table.name}.{column.name}'] = column.sync

            for column_info in column_infos:
                if judge_sync[column_info.id]:
                    values = await self.datarepo_mysql_operate.get_columns_values(column_info.table_id,column_info.name,1000)
                    document = [ValueInfo(
                        id=f'{column_info.id}.{value}',
                        value=value,
                        column_id=column_info.id,
                    ) for value in values]
                    documents.extend(document)

            await self.es_operate.add(documents)
        except Exception as e:
            logger.error(f"Meta Service -- ES 存储column值数据失败:{e}")


    async def _save_metric_info_to_meta_db(self):
        try:
            metric_infos = []
            column_metrics = []
            for metric in self.meta_config.metrics:
                metric_info = MetricInfo(
                    id = metric.name,
                    name = metric.name,
                    description = metric.description,
                    relevant_columns = metric.relevant_columns,
                    alias = metric.alias
                )
                metric_infos.append(metric_info)

                for relevant_column in metric.relevant_columns:
                    column_metric = ColumnMetric(
                        column_id=relevant_column,
                        metric_id=metric.name,
                    )

                    column_metrics.append(column_metric)

            async with self.meta_mysql_operate.session.begin():
                self.meta_mysql_operate.save_metric_infos(metric_infos)
                self.meta_mysql_operate.save_column_metrics(column_metrics)

            return metric_infos
        except Exception as e:
            logger.error(f"Meta Service -- MySQL meta存储metric数据失败:{e}")


    async def _save_metric_info_to_qdrant(self,metric_infos:list[MetricInfo]):
        """把字段的name、description、alias放进库中"""
        try:
            await self.metric_qdrant_operate.confirm_collection()
            points:list[PointStruct] = []
            for metric_info in metric_infos:
                elements = []
                embeddings = []
                elements.extend([metric_info.name,metric_info.description])
                elements.extend([alia for alia in metric_info.alias])
                logger.info(f"Qdrant数据{metric_info.name}进行批量向量化处理中...")
                for element in elements:
                    embed = await self.embed_operate.embed(element)
                    embeddings.extend(embed)
                points.extend([PointStruct(id=uuid4(),vector=embedding,payload=asdict(metric_info)) for embedding in embeddings])

            await self.metric_qdrant_operate.upsert(points)
        except Exception as e:
            logger.error(f"Meta Service -- Qdrant 存储metric数据失败:{e}")


    async def build(self):
        """元数据构建总入口"""

        #检查metadata数据库表是否已建立
        logger.info(f"元数据数据库表检查...")
        self.meta_mysql_operate.confirm_meta_db_tables()


        logger.info(f"元数据库开始加载配置")
        if self.meta_config.tables:
            logger.info("检测到配置文件已配置tables内容，开始进行元数据库tables构建")
            column_infos = await self._save_tables_to_meta_db()
            await self._save_column_info_to_qdrant(column_infos)
            await self._save_value_info_to_es(column_infos)

        if self.meta_config.metrics:
            logger.info("检测到配置文件已配置metrics内容，开始进行元数据库metrics构建")
            metric_infos = await self._save_metric_info_to_meta_db()
            await self._save_metric_info_to_qdrant(metric_infos)

        logger.info(f"已完成元数据库构建")










































