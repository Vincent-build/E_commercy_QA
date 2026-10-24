import jieba
from qa_process.agent.LangGraph_state.state_schema import DataAgentState
from qa_process.agent.LangGraph_context.context_schema import ProcessContext
from langgraph.runtime import Runtime
from pathlib import Path


def  extract_keywords(state:DataAgentState,runtime:Runtime[ProcessContext]):
    writer = runtime.stream_writer
    step = "提取关键词信息"
    writer({"step": step, "status": "running"})

    try:
        path_ = Path(__file__).parents[0] / "stopwords.txt"
        query = state["query"]
        allow_part_of_speech = (
            "n",  # 名词：商品、订单、销售额
            "nr",  # 人名：张三、李四
            "ns",  # 地名：华北、北京、上海
            "nt",  # 机构团体名：门店、品牌、渠道
            "nz",  # 其他专有名词：SKU、GMV、AOV
            "v",  # 动词：统计、对比、查询
            "vn",  # 名动词：销售、成交、退款
            "a",  # 形容词：新增、有效、活跃
            "an",  # 名形词：可用、有效、异常
            "eng",  # 英文：GMV、SKU、ROI
            "i",  # 成语或习用语，避免遗漏整体表达
            "l",  # 常用固定短语，例如“销售总额”
        )
        jieba.load_userdict(allow_part_of_speech)
        keywords = jieba.lcut(query)

        with open(path_,'r',encoding="utf-8") as f:
            swds = f.readlines()

        stopwords = [word.replace("\n","") for word in swds]

        new_keywords = []

        for keyword in keywords:
            if keyword not in stopwords:
                new_keywords.append(keyword)

        keywords = list(set(new_keywords + [query]))

        return {"keywords":keywords}

    except Exception as e:
        writer({"step":step,"status":"error","detail":str(e)})


























