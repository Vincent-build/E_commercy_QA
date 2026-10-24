from dataclasses import dataclass

#用于对应数仓ORM格式结构

@dataclass
class FactOrder:
    order_id:str
    customer_id:str
    product_id:str
    date_id:int
    region_id:str
    order_quantity:int
    order_amount:float


@dataclass
class DimRegion:
    region_id:str
    province:str
    region_name:str
    country:str


@dataclass
class DimCustomer:
    customer_id:str
    customer_name:str
    gender:str
    member_level:str



@dataclass
class DimProduct:
    product_id:str
    product_name:str
    category:str
    brand:str


@dataclass
class DimDate:
    date_id:int
    year:int
    quarter:str
    month:int
    day:int