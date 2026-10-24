from qa_process.agent.LangGraph_state.state_schema import DataAgentState
from qa_process.agent.LangGraph_context.context_schema import ProcessContext
from qa_process.prompt_loader.load_prompt import load_prompt
from qa_process.agent.LangChain_llm.llm import llm
from langchain_core.output_parsers import StrOutputParser
from langgraph.runtime import Runtime


async def generate_sql(state:DataAgentState,runtime:Runtime[ProcessContext]):
    writer = runtime.stream_writer
    step = "生成SQL"
    writer({"step":step,"status":"running"})


    query = state["query"]
    table_infos = state["table_infos"]
    metric_infos = state["metric_infos"]
    date_info = state["date_info"]
    db_info = state["db_info"]

    prompt = load_prompt("generate_sql")

    chain = prompt | llm | StrOutputParser()

    try:

        sql = await chain.ainvoke({
            "query":query,
            "table_infos":table_infos,
            "metric_infos":metric_infos,
            "date_info":date_info,
            "db_info":db_info,
        })

    except Exception as e:
        writer({"step": step, "process": "generate_sql", "status": "error", "detail": str(e)})


    #进入校验流程前，先把状态清零
    state["retry_time"] = 0

    writer({"step": step, "status": "success"})
    writer({"generate_sql":sql})

    return {"sql":sql}
















