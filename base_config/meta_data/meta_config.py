"""
用于写入时配合脚本一起
"""

from dataclasses import dataclass
from typing import Optional
from omegaconf import OmegaConf
from pathlib import Path

@dataclass
class MetricConfig:
    name:str
    role:str
    description:str
    relevant_columns:list[str]
    alias:list[str]

@dataclass
class TableConfig:
    name:str
    role:str
    description:str
    columns:list[ColumnConfig]

@dataclass
class ColumnConfig:
    name:str
    role:str
    description:str
    alias:list[str]
    sync:bool

@dataclass
class MetaConfig:
    tables:Optional[list[TableConfig]] = None
    metrics:Optional[list[MetricConfig]] = None

path_ = Path(__file__).parents[0] / "meta_config.yaml"

structured = OmegaConf.structured(MetaConfig)

schema = OmegaConf.load(path_)

merged = OmegaConf.merge(structured,schema)

meta_config:MetaConfig = OmegaConf.to_object(merged)

if __name__ == "__main__":
    for table in meta_config.tables:
        columns = table.columns
        for column in columns:
            print(column.name)






