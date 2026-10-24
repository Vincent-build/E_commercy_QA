from qa_process.agent.LangGraph_state.state_schema import DataAgentState
from qa_process.agent.LangGraph_context.context_schema import ProcessContext
from langgraph.runtime import Runtime
from qa_process.agent.LangGraph_state.state_schema import DBInfoState,DateInfoState
from datetime import date


async def add_extra_context(state:DataAgentState,runtime:Runtime[ProcessContext]):
    writer = runtime.stream_writer
    step = "增加额外字段信息"
    writer({"step":step,"status":"running"})

    try:
        datarepo_mysql_operate = runtime.context["datarepo_mysql_operate"]

        today = date.today()
        date_str = today.strftime("%Y-%m-%d")
        weekday = today.strftime("%A")
        quarter = f"Q{(today.month -1) //3 +1}"
        date_info = DateInfoState(
            date=date_str,
            weekday=weekday,
            quarter=quarter,
        )

        db_version = await datarepo_mysql_operate.get_db_info()

        db_info = DBInfoState(**db_version)

        writer({"step": step, "status": "success"})

        return {"date_info":date_info,"db_info":db_info}

    except Exception as e:
        writer({"step":step,"process":"add_extra_context","status":"error","detail":str(e)})












