from fastapi import FastAPI,Request
from api.life_span.lifespan import lifespan
from api.qa_router.fastapi_router import api_router,mysql_router
from uuid import uuid4
from api.async_context.context import request_id_ctx_var


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
app.include_router(mysql_router)

@app.middleware("http")
async def add_request_id(request:Request,call_next):

    request_id = uuid4()

    request_id_ctx_var.set(request_id)

    response = await call_next(request)

    return response

import uvicorn
uvicorn.run(app,host="127.0.0.1",port=8080)