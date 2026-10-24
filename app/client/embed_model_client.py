from base_config.config.app_config import config as conf
from base_config.log.logger import logger
import httpx2
from typing import Optional
import asyncio

class EmbeddingManagement:
    def __init__(self,
                 host=conf.embed_model.host,
                 port=conf.embed_model.port):
        self.host = host
        self.port = port
        self.client:Optional[httpx2.AsyncClient]=None

    def _get_url(self):
        return f"http://{self.host}:{self.port}"

    def init(self):
        try:
            url = self._get_url()
            self.client = httpx2.AsyncClient(base_url=url)
            logger.info(f"初始化嵌入模型服务器完成")
        except Exception as e:
            logger.error(f"初始化嵌入模型服务器失败:{e}")

    async def close(self):
        await self.client.aclose()
        logger.info(f"Embedding服务器关闭")


embedding_client_management = EmbeddingManagement()

if __name__ == "__main__":
    async def main():
        await embedding_client_management.init()
        client = embedding_client_management.client

    asyncio.run(main())