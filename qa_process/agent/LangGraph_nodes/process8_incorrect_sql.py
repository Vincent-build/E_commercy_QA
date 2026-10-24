from qa_process.agent.LangGraph_state.state_schema import DataAgentState
from qa_process.agent.LangGraph_context.context_schema import ProcessContext
from qa_process.agent.LangChain_llm.llm import llm
from qa_process.prompt_loader.load_prompt import load_prompt
from langchain_core.output_parsers import StrOutputParser
from langgraph.runtime import Runtime
from langgraph.types import Command
from base_config.log.logger import logger


async def incorrect_sql(state:DataAgentState,runtime:Runtime[ProcessContext]):
    writer = runtime.stream_writer
    step = "校正SQL"
    writer({"step":step,"status":"running"})

    query = state["query"]
    error = state["error"]
    sql = state["sql"]
    table_infos = state["table_infos"]
    metric_infos = state["metric_infos"]
    date_info = state["date_info"]
    db_info = state["db_info"]

    prompt = load_prompt("incorrect_sql")

    chain = prompt | llm | StrOutputParser()

    try:
        incorrect_sql_text = await chain.ainvoke({
            "query":query,
            "error":error,
            "sql":sql,
            "table_infos":table_infos,
            "metric_infos":metric_infos,
            "date_info":date_info,
            "db_info":db_info,
        })
    except Exception as e:
        writer({"step": step, "process": "incorrect_sql", "status": "error", "detail": str(e)})


    writer({"step": step, "status": "running"})

    return Command(
        update={"sql":incorrect_sql_text},
        goto="validate_sql"
    )











