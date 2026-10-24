from qa_process.agent.LangGraph_state.state_schema import DataAgentState
from qa_process.agent.LangGraph_context.context_schema import ProcessContext
from qa_process.prompt_loader.load_prompt import load_prompt
from qa_process.agent.LangChain_llm.llm import llm
from langchain_core.output_parsers import JsonOutputParser
from langgraph.runtime import Runtime
from base_config.log.logger import logger

async def recall_metric_info(state:DataAgentState,runtime:Runtime[ProcessContext]):
    writer = runtime.stream_writer
    step = "召回指标信息"
    writer({"step":step,"status":"running"})

    try:
        query = state["query"]
        keywords = state["keywords"]

        prompt = load_prompt("extend_keywords_for_metric_recall")

        chain = prompt | llm | JsonOutputParser()

        extend_keywords = await chain.ainvoke({"query":query})

        keywords = list(set(keywords + extend_keywords))

        qdrant_metric_recall = runtime.context["metric_qdrant_operate"]
        embed_operate = runtime.context["embed_operate"]

        logger.info("P2_metric 开始处理关键词向量化...")

        embeds = []
        for keyword in keywords:
            embed = await embed_operate.embed(keyword)
            embeds.extend(embed)

        logger.info("P2_metric 开始处理Qdrant召回...")

        metric_infos = {}
        for embed in embeds:
            metrics = await qdrant_metric_recall.search_points(embed)
            if metrics:
                for metric in metrics:
                    metric_infos[metric.id] = metric

        metric_list = [value for _,value in metric_infos.items()]

        writer({"step": step, "status": "success"})

        return {"retrieval_metric_infos":metric_list}

    except Exception as e:
        writer({"step":step,"status":"error","detail":str(e)})
























