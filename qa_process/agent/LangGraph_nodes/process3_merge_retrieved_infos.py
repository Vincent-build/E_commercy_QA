from sys import orig_argv

from qa_process.agent.LangGraph_state.state_schema import DataAgentState
from qa_process.agent.LangGraph_context.context_schema import ProcessContext
from qa_process.prompt_loader.load_prompt import load_prompt
from qa_process.agent.LangGraph_state.state_schema import ColumnInfoState,TableInfoState,MetricInfoState
from app.database_entity.table_info import TableInfo
from langgraph.runtime import Runtime
from base_config.log.logger import logger


async def merge_retrieval_info(state:DataAgentState,runtime:Runtime[ProcessContext]):
    writer = runtime.stream_writer
    step = "合并召回信息"
    writer({"step":step,"status":"running"})

    column_infos = state["retrieval_column_infos"]
    metric_infos = state["retrieval_metric_infos"]
    value_infos = state["retrieval_column_values"]
    meta_mysql_operate = runtime.context["meta_mysql_operate"]

    #流程：字段召回 + 指标依赖字段 + 字段真实取值 + 主外键补齐
    distinct_retrieval_column_infos = {}

    try:
        #字段召回，补齐上下文
        for column_info in column_infos:
            ids = column_info.id
            column_info = await meta_mysql_operate.get_column_info(ids)
            distinct_retrieval_column_infos[column_info.id] = column_info
    except Exception as e:
        writer({"step": step,"process": "metric_column","status": "error","detail":str(e)})


    try:
        #指标依赖字段信息召回
        for metric_info in metric_infos:
            relevant_columns = metric_info.relevant_columns
            if relevant_columns:
                for relevant_column in relevant_columns:
                    column_info = await meta_mysql_operate.get_column_info(relevant_column)
                    distinct_retrieval_column_infos[column_info.id] = column_info
    except Exception as e:
        writer({"step": step, "process": "merge_metric", "status": "error", "detail": str(e)})


    try:
        #字段真实取值
        for value_info in value_infos:
            value = value_info.value
            column_id = value_info.column_id
            column_info = await meta_mysql_operate.get_column_info(column_id)
            distinct_retrieval_column_infos[column_info.id] = column_info
            if value not in distinct_retrieval_column_infos[column_info.id].examples:
                distinct_retrieval_column_infos[column_info.id].examples.append(value)
    except Exception as e:
        writer({"step": step, "process": "merge_value", "status": "error", "detail": str(e)})


    try:
        #整理全部上下文
        organize_retrieval_column_infos: dict[str, list] = {}
        recall_infos = [value for _,value in distinct_retrieval_column_infos.items()]
        for info in recall_infos:
            table_ids = info.table_id
            if organize_retrieval_column_infos.get(table_ids):
                organize_retrieval_column_infos[table_ids].append(info)
            else:
                organize_retrieval_column_infos[table_ids] = [info]
    except Exception as e:
        writer({"step": step, "process": "organize_context", "status": "error", "detail": str(e)})


    try:
        #召回主外键且合并
        key_roles = []
        for key_info in organize_retrieval_column_infos.keys():
            column_role = await meta_mysql_operate.get_key_columns(key_info)
            key_roles.extend(column_role)

        column_mes = [value for _,value in organize_retrieval_column_infos.items()]

        for column_role in key_roles:
            if column_role not in column_mes:
                table_ids = column_role.table_id
                if organize_retrieval_column_infos.get(table_ids):
                    organize_retrieval_column_infos[table_ids].append(column_role)
                else:
                    organize_retrieval_column_infos[table_ids] = [column_role]
    except Exception as e:
        writer({"step": step, "process": "keys_recall", "status": "error", "detail": str(e)})


    try:
        #生成Column_info上下文
        table_info_state = []
        for table_id,column_infos in organize_retrieval_column_infos.items():
            table_infos:TableInfo = await meta_mysql_operate.get_table_info(table_id)
            columns = [ColumnInfoState(
                name=column_info.name,
                type=column_info.type,
                role=column_info.role,
                examples=column_info.examples,
                description=column_info.description,
                alias=column_info.alias,
            ) for column_info in column_infos]

            table_info = TableInfoState(
                name=table_infos.name,
                description=table_infos.description,
                role=table_infos.role,
                columns=columns,
            )
            table_info_state.append(table_info)
    except Exception as e:
        writer({"step": step, "process": "generate_column_context", "status": "error", "detail": str(e)})


    try:
        #生成Metric_info上下文
        metric_info_state:list[MetricInfoState] = [MetricInfoState(
            name=metric_info.name,
            description=metric_info.description,
            relevant_columns=metric_info.relevant_columns,
            alias=metric_info.relevant_columns
        ) for metric_info in metric_infos ]
    except Exception as e:
        writer({"step": step, "process": "generate_metric_context", "status": "error", "detail": str(e)})

    writer({"step": step, "status": "success"})

    return {"table_infos":table_info_state,"metric_infos":metric_info_state}









