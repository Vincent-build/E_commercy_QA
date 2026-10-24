import asyncio
from base_config.log.logger import logger

from langgraph.graph import StateGraph
from langgraph.types import RetryPolicy

from qa_process.agent.LangGraph_nodes.process1_extract_keywords import extract_keywords
from qa_process.agent.LangGraph_nodes.process2_recall_column import recall_column_info
from qa_process.agent.LangGraph_nodes.process2_recall_metric import recall_metric_info
from qa_process.agent.LangGraph_nodes.process2_recall_value import recall_value_info
from qa_process.agent.LangGraph_nodes.process3_merge_retrieved_infos import merge_retrieval_info
from qa_process.agent.LangGraph_nodes.process4_filter_metric import filter_metric
from qa_process.agent.LangGraph_nodes.process4_fliter_table import filter_table
from qa_process.agent.LangGraph_nodes.process5_add_extra_context import add_extra_context
from qa_process.agent.LangGraph_nodes.process6_generate_sql import generate_sql
from qa_process.agent.LangGraph_nodes.process7_validate_sql import validate_sql
from qa_process.agent.LangGraph_nodes.process8_incorrect_sql import incorrect_sql
from qa_process.agent.LangGraph_nodes.process9_run_sql import run_sql
from qa_process.agent.LangGraph_nodes.process10_print_answer import print_answer

from qa_process.agent.LangGraph_context.context_schema import ProcessContext
from qa_process.agent.LangGraph_state.state_schema import DataAgentState



async def graph_process():
    build = StateGraph(state_schema=DataAgentState,context_schema=ProcessContext)
    build.add_node("extract_keywords",extract_keywords)
    build.add_node("recall_column_info",recall_column_info)
    build.add_node("recall_metric_info",recall_metric_info)
    build.add_node("recall_value_info",recall_value_info)
    build.add_node("merge_retrieval_info",merge_retrieval_info)
    build.add_node("filter_metric",filter_metric)
    build.add_node("filter_table",filter_table)
    build.add_node("add_extra_context",add_extra_context)
    build.add_node("generate_sql",generate_sql)
    build.add_node("validate_sql",validate_sql,retry_policy=RetryPolicy(max_attempts=3,jitter=True))
    build.add_node("incorrect_sql",incorrect_sql)
    build.add_node("run_sql",run_sql)
    build.add_node("print_answer",print_answer)

    build.set_entry_point("extract_keywords")
    build.add_edge("extract_keywords","recall_metric_info")
    build.add_edge("extract_keywords","recall_column_info")
    build.add_edge("extract_keywords","recall_value_info")
    build.add_edge("recall_column_info","merge_retrieval_info")
    build.add_edge("recall_column_info","merge_retrieval_info")
    build.add_edge("recall_value_info","merge_retrieval_info")
    build.add_edge("merge_retrieval_info","filter_metric")
    build.add_edge("merge_retrieval_info","filter_table")
    build.add_edge("filter_metric","add_extra_context")
    build.add_edge("filter_table","add_extra_context")
    build.add_edge("add_extra_context","generate_sql")
    build.add_edge("generate_sql","validate_sql")
    build.add_conditional_edges(
        source="validate_sql",
        path=lambda state:"run_sql" if state["error"] is None else "incorrect_sql",
        path_map={"incorrect_sql":"incorrect_sql","run_sql":"run_sql"}
    )
    build.add_edge("incorrect_sql", "validate_sql")
    build.add_edge("validate_sql","run_sql")
    build.add_edge("run_sql","print_answer")
    build.set_finish_point("print_answer")

    graph = build.compile()

    logger.info("图流程加载完毕...")

    return graph


if __name__ == "__main__":
    asyncio.run(graph_process())













