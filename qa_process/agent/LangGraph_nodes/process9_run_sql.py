from langgraph.runtime import Runtime
from qa_process.agent.LangGraph_state.state_schema import DataAgentState
from qa_process.agent.LangGraph_context.context_schema import ProcessContext

async def run_sql(state:DataAgentState,runtime:Runtime[ProcessContext]):
    writer = runtime.stream_writer
    step = "运行SQL"
    writer({"step":step,"status":"running"})

    datarepo_operate = runtime.context["datarepo_mysql_operate"]

    sql = state["sql"]

    try:
        result = await datarepo_operate.run_sql(sql)
    except Exception as e:
        writer({"step": step, "process": "run_sql", "status": "error", "detail": str(e)})

    writer({"step": step, "status": "success"})

    return {"answer":result}




