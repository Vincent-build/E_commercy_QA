from qa_process.agent.LangGraph_context.context_schema import ProcessContext
from qa_process.agent.LangGraph_state.state_schema import DataAgentState
from langgraph.runtime import Runtime
from base_config.log.logger import logger

async def print_answer(state:DataAgentState,runtime:Runtime[ProcessContext]):

    writer = runtime.stream_writer

    logger.info(f"问题: {state["query"]} ||  回答 : {state["answer"]}")
    writer({"问题": state["query"], "回答": state["answer"]})

    return state