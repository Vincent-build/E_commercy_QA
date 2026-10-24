from fastapi import APIRouter,Depends
from api.service_dependencies.dependencies import get_query_service,QueryService
from api.query_schema.query_schema import QuerySchema
from typing import Annotated
from starlette.responses import StreamingResponse

from app.services.data_repository_update_service import DataRepositoryUpdate
from app.services.meta_knowledge_service import MetaKnowledgeService
from api.service_dependencies.dependencies import get_meta_service,update_datarepo_service


api_router = APIRouter(prefix="/api")

#SSE通信
@api_router.post("/query")
async def query_handler(query:QuerySchema,query_service:Annotated[QueryService,Depends(get_query_service)]):
    return StreamingResponse(
        query_service.query(query.query),
        media_type="text/event_stream"
    )



mysql_router = APIRouter(prefix="/mysql")

@mysql_router.post("/update")
async def update_sql(
        datarepo_update_service: Annotated[DataRepositoryUpdate, Depends(update_datarepo_service)],
):
    datarepo_update_service.update()


@mysql_router.post("/write")
async def write_sql(
        metadata_write_in: Annotated[MetaKnowledgeService, Depends(get_meta_service)],
):
    await metadata_write_in.build()











