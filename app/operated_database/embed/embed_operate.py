"""
向量化
"""
import json
from base_config.config.app_config import config as conf
from base_config.log.logger import logger
import asyncio

class EmbeddingOperatiion:
    def __init__(self,embed_client):
        self.client = embed_client
        self.host = conf.embed_model.host
        self.port = conf.embed_model.port

    def _get_url(self):
        return f"http://{self.host}:{self.port}"

    async def embed(self,query:str):
        try:
            headers = {"Content-Type":"application/json"}
            embed_query = json.dumps({"inputs":query}).encode()
            url = self._get_url()
            embeddings = await self.client.request("POST",url=url,content=embed_query,headers=headers,timeout=100)
            return json.loads(embeddings.content)
        except Exception as e:
            logger.error(f"Embed Operate 嵌入模型向量化失败：{e}")

if __name__ == "__main__":
    async def main():
        from app.client.embed_model_client import embedding_client_management
        await embedding_client_management.init()
        client = embedding_client_management.client
        e = EmbeddingOperatiion(client)
        result = await e.embed("Python是什么")
        print(result)

    asyncio.run(main())
























