from qa_process.agent.LangChain_llm.llm import llm
from qa_process.agent.LangGraph_context.context_schema import ProcessContext
from qa_process.agent.LangGraph_state.state_schema import DataAgentState
from qa_process.prompt_loader.load_prompt import load_prompt
from langgraph.runtime import Runtime
from langchain_core.output_parsers import JsonOutputParser
import yaml

async def filter_table(state:DataAgentState,runtime:Runtime[ProcessContext]):
    writer = runtime.stream_writer
    step = "过滤表信息"
    writer({"step":step,"status":"running"})

    query = state["query"]

    table_infos = state["table_infos"]

    prompt = load_prompt("filter_table_info")

    chain = prompt | llm | JsonOutputParser()

    try:
        table_info_filter = await chain.ainvoke({"query":query,"table_infos":yaml.dump(table_infos,allow_unicode=True,sort_keys=False)})
    except Exception as e:
        writer({"step": step, "process": "filter_table", "status": "error", "detail": str(e)})

    table_infos_filter = [table_info for table_info in table_infos if table_info["name"] in table_info_filter]

    writer({"step": step, "status": "success"})

    return {"table_infos":table_infos_filter}









