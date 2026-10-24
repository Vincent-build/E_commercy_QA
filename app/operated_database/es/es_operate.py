"""
创建索引
插入文档
搜索文档
"""
from base_config.config.app_config import config as conf
from base_config.log.logger import logger
from uuid import uuid4
from dataclasses import asdict
from app.database_entity.value_info import ValueInfo




class ESOperation:
    mappings = {
        "dynamic": False,
        "properties": {
            "id": {"type": "keyword"},
            "value": {
                "type": "text",
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_max_word",
            },
            "column_id": {"type": "keyword"}
        }
    }
    def __init__(self,es_client):
        self.client = es_client
        self.index_name = conf.elasticsearch.index_name

    async def confirm_index(self):
        try:
            if not await self.client.indices.exists(index=self.index_name):
                await self.client.indices.create(index=self.index_name,mappings=self.mappings)
                logger.info(f"ES 已建立索引{self.index_name}")
        except Exception as e:
            logger.error(f"ES operate 创建索引失败:{e}")


    async def add(self,documents:list[ValueInfo]):
        try:
            if not await self.client.indices.exists(index=self.index_name):
                logger.warning(f"ES operate ES不存在索引{self.index_name}")
                return
            if not documents:
                logger.warning(f"ES operate 请求存入ES的数据为空")
                return

            actions = []
            for document in documents:
                actions.extend([{"index":{"_index":f"{self.index_name}","_id":document.id}},asdict(document)])

            await self.client.bulk(
                index=self.index_name,operations=actions
            )
        except Exception as e:
            logger.error(f"ES operate ES存入数据异常:{e}")


    async def search(self,
               keyword:str,
               limit=conf.elasticsearch.limit,
               threshold=conf.elasticsearch.threshold
    ):
        query = {
            "query":{
                "match":{
                    "value":f"{keyword.strip()}"
                }
            }
        }
        result = await self.client.search(index=self.index_name,body=query,size=limit,min_score=threshold)
        return [ValueInfo(**source["_source"]) for source in result["hits"]["hits"]]














