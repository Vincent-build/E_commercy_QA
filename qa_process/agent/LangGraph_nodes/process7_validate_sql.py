from qa_process.agent.LangGraph_context.context_schema import ProcessContext
from qa_process.agent.LangGraph_state.state_schema import DataAgentState
from langgraph.runtime import Runtime
from base_config.log.logger import logger


async def validate_sql(state:DataAgentState,runtime:Runtime[ProcessContext]):
    writer = runtime.stream_writer
    step = "校验SQL"
    writer({"step":step,"status":"running"})

    sql = state["sql"]

    datarepo_mysql_operate = runtime.context["datarepo_mysql_operate"]

    result,mes = await datarepo_mysql_operate.validate_sql(sql)

    if result:
        writer({"step":step,"status":"success"})
        logger.info(f"生成的SQL语法正确")
        return {"error":None}
    else:
        writer({"step": step, "status": "success"})
        logger.info(f"生成的SQL语法错误")
        if state["retry_time"] == 3:
            logger.error(f"已超出SQL校验次数，请自行检查数据库内容...")
            raise SystemExit(f"已超出SQL校验次数，请自行检查数据库内容...")
        return {"error":mes,"retry_time":1}



