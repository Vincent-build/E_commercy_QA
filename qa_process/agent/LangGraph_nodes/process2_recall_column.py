from qa_process.agent.LangGraph_state.state_schema import DataAgentState
from qa_process.agent.LangGraph_context.context_schema import ProcessContext
from qa_process.prompt_loader.load_prompt import load_prompt
from langgraph.runtime import Runtime
from langchain_core.output_parsers import JsonOutputParser
from qa_process.agent.LangChain_llm.llm import llm
from base_config.log.logger import logger


async def recall_column_info(state:DataAgentState,runtime:Runtime[ProcessContext]):
    writer = runtime.stream_writer
    step = "召回字段信息"
    writer({"step":step,"status":"running"})

    try:
        query = state["query"]

        prompt = load_prompt("extend_keywords_for_column_recall")

        chain = prompt | llm | JsonOutputParser()

        extend_keywords = await chain.ainvoke({"query":query})

        keywords = state["keywords"]

        keywords = set(keywords + extend_keywords)

        qdrant_column_recall = runtime.context["column_qdrant_operate"]

        embedding_operate = runtime.context["embed_operate"]

        logger.info("P2_column 开始处理关键词向量化...")

        embed_list = []
        for kw in keywords:
            embed = await embedding_operate.embed(kw)
            embed_list.extend(embed)

        logger.info("P2_column 开始处理Qdrant召回...")

        column_infos = {}
        for embedding in embed_list:
            column_info_mes = await qdrant_column_recall.search_points(embedding)
            if column_info_mes:
                for column_info in column_info_mes:
                    column_infos[column_info.id] = column_info

        column_list = [value for _,value in column_infos.items()]

        writer({"step": step, "status": "success"})

        return {"retrieval_column_infos":column_list}

    except Exception as e:
        writer({"step":step,"status":"error","detail":str(e)})


if __name__ == "__main__":
    pass













