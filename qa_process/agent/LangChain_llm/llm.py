from langchain.chat_models import init_chat_model
from base_config.config.app_config import config as conf


llm = init_chat_model(
    api_key = conf.llm.api_key,
    model = conf.llm.model_name,
    base_url = conf.llm.base_url,
    model_provider= conf.llm.model_provider,
    temperature = conf.llm.temperature
)
















