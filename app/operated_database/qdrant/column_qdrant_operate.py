"""
创建集
插入点
召回检索
"""
from base_config.config.app_config import config as conf
from qdrant_client.models import VectorParams,Distance,PointStruct
from base_config.log.logger import logger
from app.database_entity.column_info import ColumnInfo


class QdrantColumnOperation:
    def __init__(self,qdrant_client):
        self.client = qdrant_client
        self.collection_name = conf.qdrant.column_collection_name
        self.dim = conf.qdrant.dim
        self.k = conf.qdrant.search_k
        self.score_threshold = conf.qdrant.score_threshold



    async def confirm_collection(self):
        try:
            if not await self.client.collection_exists(self.collection_name):
                await self.client.create_collection(
                    self.collection_name,
                    vectors_config=VectorParams(
                    size=self.dim,
                    distance=Distance.COSINE)
                    )
                logger.info(f"创建集{self.collection_name}完成")
            logger.info(f"已加载{self.collection_name}集")
        except Exception as e:
            logger.error(f"Qdrant Operate 创建集失败:{e}")


    async def upsert(self,points:list[PointStruct]):
        try:

            logger.info(f"Qdrant存入points流程")
            await self.client.upsert(collection_name=self.collection_name,
                            points=points)
        except Exception as e:
            logger.error(f"Qdrant Operate {self.collection_name}集插入point失败:{e}")


    async def search_points(self,embedding:list[float]):
        try:
            logger.info(f"Qdrant开始检索")
            result = await self.client.query_points(
                collection_name=self.collection_name,
                query=embedding,
                limit=self.k,
                score_threshold=self.score_threshold,
                with_payload=True
            )
            if result:
                logger.info("Qdrant已召回检索内容")
                return [ColumnInfo(**point.payload) for point in result.points]
            else:
                logger.warning("Qdrant检索召回失败")
        except Exception as e:
            logger.error(f"Qdrant Operate {self.collection_name}检索失败:{e}")






















