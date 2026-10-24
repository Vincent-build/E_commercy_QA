from dataclasses import dataclass
from omegaconf import OmegaConf
from pathlib import Path

#用于获取配置文件中的数仓数据

@dataclass
class FactOrder:
    order_id:list[str]
    customer_id:list[str]
    product_id:list[str]
    date_id:list[int]
    region_id:list[str]
    order_quantity:list[int]
    order_amount:list[float]


@dataclass
class DimRegion:
    region_id:list[str]
    province:list[str]
    region_name:list[str]
    country:list[str]


@dataclass
class DimCustomer:
    customer_id:list[str]
    customer_name:list[str]
    gender:list[str]
    member_level:list[str]



@dataclass
class DimProduct:
    product_id:list[str]
    product_name:list[str]
    category:list[str]
    brand:list[str]


@dataclass
class DimDate:
    date_id:list[int]
    year:list[int]
    quarter:list[str]
    month:list[int]
    day:list[int]


@dataclass
class DataRepository:
    fact_order:FactOrder
    dim_customer:DimCustomer
    dim_region:DimRegion
    dim_date:DimDate
    dim_product:DimProduct


path_ = Path(__file__).parents[0] / "datarepo_from_config.yaml"

structured = OmegaConf.structured(DataRepository)

schema = OmegaConf.load(path_)

merged = OmegaConf.merge(structured,schema)

data_repository_config:DataRepository = OmegaConf.to_object(merged)

if __name__ == "__main__":
    print(data_repository_config.fact_order.date_id)





