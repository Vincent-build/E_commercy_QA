from dataclasses import dataclass
from omegaconf import OmegaConf
from pathlib import Path



@dataclass
class MySQL:
    host:str
    port:str
    user:str
    password:str
    database:str


@dataclass
class Qdrant:
    host:str
    port:str
    dim:int
    column_collection_name:str
    metric_collection_name:str
    search_k:int
    score_threshold:float

@dataclass
class Elasticsearch:
    host:str
    port:str
    auth_user:str
    auth_password:str
    index_name:str
    limit:int
    threshold:float


@dataclass
class Embed_model:
    host:str
    port:str
    model_path:str


@dataclass
class LLM:
    model_name:str
    api_key:str
    base_url:str
    model_provider:str
    temperature:float


@dataclass
class AppConfig:
    mysql_meta:MySQL
    mysql_dr:MySQL
    qdrant:Qdrant
    elasticsearch:Elasticsearch
    embed_model:Embed_model
    llm:LLM


path_ = Path(__file__).parents[0] / "app_config.yaml"

structured_ = OmegaConf.structured(AppConfig)
schema = OmegaConf.load(path_)
merge = OmegaConf.merge(structured_,schema)
config:AppConfig = OmegaConf.to_object(merge)

if __name__ == "__main__":
    print(config.mysql_dr.host)


























