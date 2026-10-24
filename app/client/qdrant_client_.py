from qdrant_client import AsyncQdrantClient
from base_config.config.app_config import config as conf
from base_config.log.logger import logger
import asyncio



class QdrantManagement:
    def __init__(self,
                 host=conf.qdrant.host,
                 port=conf.qdrant.port
    ):
        self.host = host
        self.port = port
        self.client = None

    def _get_url(self):
        return f"http://{self.host}:{self.port}"

    def init(self):
        try:
            url = self._get_url()
            self.client = AsyncQdrantClient(url=url)
            logger.info(f"初始化Qdrant服务器完成")
        except Exception as e:
            logger.error(f"初始化Qdrant服务器失败:{e}")


    async def close(self):
        await self.client.close()
        logger.info(f"Qdrant服务器关闭")

qdrant_client_management = QdrantManagement()

if __name__ == "__main__":
    async def main():
        await qdrant_client_management.init()

    asyncio.run(main())















