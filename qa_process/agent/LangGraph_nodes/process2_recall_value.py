from qa_process.agent.LangChain_llm.llm import llm
from qa_process.agent.LangGraph_context.context_schema import ProcessContext
from qa_process.agent.LangGraph_state.state_schema import DataAgentState
from qa_process.prompt_loader.load_prompt import load_prompt
from langchain_core.output_parsers import JsonOutputParser
from langgraph.runtime import Runtime
from base_config.log.logger import logger



async def recall_value_info(state:DataAgentState,runtime:Runtime[ProcessContext]):

    writer = runtime.stream_writer
    step = "召回字段值信息"
    writer({"step":step,"status":"running"})

    try:

        query = state["query"]
        keywords = state["keywords"]

        prompt = load_prompt("extend_keywords_for_value_recall")

        chain = prompt | llm | JsonOutputParser()

        extend_keywords = await chain.ainvoke({"query":query})

        keywords = list(set(keywords + extend_keywords))

        es_operate = runtime.context["es_operate"]

        logger.info("P2_value 开始处理ES召回...")

        value_infos = {}
        for keyword in keywords:
            value_info_mes = await es_operate.search(keyword)
            if value_info_mes:
                for value_info in value_info_mes:
                    value_infos[value_info.id] = value_info

        value_list = [value for _,value in value_infos.items()]

        writer({"step": step, "status": "success"})

        return {"retrieval_column_values":value_list}

    except Exception as e:
        writer({"step":step,"status":"error","detail":str(e)})











