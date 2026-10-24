from app.client.mysql_client import meta_mysql_client_management
from app.client.mysql_client import dr_mysql_client_management
from app.client.embed_model_client import embedding_client_management
from app.client.qdrant_client_ import qdrant_client_management
from app.client.elasticsearch_client import es_client_management

from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app:FastAPI):

    meta_mysql_client_management.init()
    meta_mysql_client_management.sync_init()
    dr_mysql_client_management.init()
    dr_mysql_client_management.sync_init()
    es_client_management.init()
    embedding_client_management.init()
    qdrant_client_management.init()

    yield

    await meta_mysql_client_management.close()
    meta_mysql_client_management.sync_close()
    await dr_mysql_client_management.close()
    dr_mysql_client_management.sync_close()
    await es_client_management.close()
    await embedding_client_management.close()
    await qdrant_client_management.close()





