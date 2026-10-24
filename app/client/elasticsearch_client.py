from elasticsearch import AsyncElasticsearch
from base_config.config.app_config import config as conf
from base_config.log.logger import logger
from pathlib import Path
import asyncio
import ssl



class ElasticsearchManagement:
    def __init__(self,
                 ssl_ca_path: Path,
                 host=conf.elasticsearch.host,
                 port=conf.elasticsearch.port,
                 auth_user=conf.elasticsearch.auth_user,
                 auth_password=conf.elasticsearch.auth_password,

    ):
        self.host = host
        self.port = port
        self.auth_user = auth_user
        self.auth_password = auth_password
        self.ssl_ca = ssl_ca_path
        self.client = None


    def _get_url(self):
        return f"https://{self.host}:{self.port}"


    def init(self):
        try:
            url = self._get_url()
            self.client = AsyncElasticsearch(hosts=url,
                                            basic_auth=(self.auth_user,self.auth_password),
                                            ssl_context=ssl.create_default_context(cafile=self.ssl_ca),
                                            max_retries=3)
            logger.info(f"初始化ES服务器完成")
        except Exception as e:
            logger.error(f"初始化ES服务器失败:{e}")


    async def close(self):
        await self.client.close()
        logger.info(f"Elasticsearch服务器关闭")



path_ = Path(__file__).parents[2] / "base_config" / "es_ssl_ca" / "certs" / "ca" / "ca.crt"
es_client_management = ElasticsearchManagement(path_)



if __name__ == "__main__":
    async def main():
        es_client_management.init()

    asyncio.run(main())


