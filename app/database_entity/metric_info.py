from dataclasses import dataclass
from typing import Any


@dataclass
class MetricInfo:
    id:str
    name:str
    description:str
    relevant_columns:list[Any]
    alias:list[Any]







