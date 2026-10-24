"""
创建集
插入point
召回检索
"""


from base_config.config.app_config import config as conf
from base_config.log.logger import logger
from qdrant_client.models import VectorParams,Distance,PointStruct
from app.database_entity.metric_info import MetricInfo



class QdrantMetricOperation:
    def __init__(self,qdrant_client):
        self.client =qdrant_client
        self.collection_name = conf.qdrant.metric_collection_name
        self.dim = conf.qdrant.dim
        self.k = conf.qdrant.search_k
        self.threshold = conf.qdrant.score_threshold


    async def confirm_collection(self):
        try:
            if not await self.client.collection_exists(self.collection_name):
                await self.client.create_collection(
                    self.collection_name,
                    vectors_config=VectorParams(
                        size=self.dim,
                        distance=Distance.COSINE)
                )
                logger.info(f"创建{self.collection_name}集完成")
            logger.info(f"已加载{self.collection_name}集")
        except Exception as e:
            logger.error(f"Qdrant Operate 创建{self.collection_name}集失败:{e}")


    async def upsert(self,points:list[PointStruct]):
        try:
            await self.client.upsert(collection_name=self.collection_name,points=points)
        except Exception as e:
            logger.error(f"Qdrant Operate 插入{self.collection_name}集数据失败:{e}")


    async def search_points(self,embeddings:list[str]):
        try:
            result = await self.client.query_points(
                collection_name=self.collection_name,
                query=embeddings,
                limit=self.k,
                score_threshold=self.threshold,
                with_payload=True,
            )
            return [MetricInfo(**point.payload) for point in result.points]
        except Exception as e:
            logger.error(f"Qdrant Operate {self.collection_name}集查询失败:{e}")


















