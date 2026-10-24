from qa_process.agent.LangGraph_state.state_schema import DataAgentState
from qa_process.agent.LangGraph_context.context_schema import ProcessContext
from langgraph.runtime import Runtime
from qa_process.prompt_loader.load_prompt import load_prompt
from langchain_core.output_parsers import JsonOutputParser
from qa_process.agent.LangChain_llm.llm import llm
import yaml


async def filter_metric(state:DataAgentState,runtime:Runtime[ProcessContext]):
    writer = runtime.stream_writer
    step = "过滤指标信息"
    writer({"step":step,"status":"running"})

    query = state["query"]

    metric_infos = state["metric_infos"]

    prompt = load_prompt("filter_metric_info")

    chain = prompt | llm | JsonOutputParser()

    try:
        choose_metric = await chain.ainvoke({"query":query,"metric_infos":yaml.dump(metric_infos,allow_unicode=True,sort_keys=False)})
    except Exception as e:
        writer({"step": step, "process": "filter_message", "status": "error", "detail": str(e)})

    metric_infos_filter = [metric_info for metric_info in metric_infos if metric_info["name"] in choose_metric]

    writer({"step": step, "status": "success"})

    return {"metric_infos":metric_infos_filter}



























