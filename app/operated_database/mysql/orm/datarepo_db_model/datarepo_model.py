from app.operated_database.mysql.orm.datarepo_db_model.base_model import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy.types import String,Integer,Float
from sqlalchemy import ForeignKey


class FactOrderMySQL(Base):

    __tablename__ = "fact_order"

    order_id:Mapped[str] = mapped_column(String(30),primary_key=True)
    customer_id:Mapped[str] = mapped_column(String(20),ForeignKey("dim_customer.customer_id"))
    product_id:Mapped[str] = mapped_column(String(20),ForeignKey("dim_product.product_id"))
    date_id:Mapped[int] = mapped_column(Integer,ForeignKey("dim_date.date_id"))
    region_id:Mapped[str] = mapped_column(String(20),ForeignKey("dim_region.region_id"))
    order_quantity:Mapped[int] = mapped_column(Integer)
    order_amount:Mapped[float] = mapped_column(Float)

    dim_product:Mapped["DimProductMySQL"] = relationship(back_populates="fact_order")
    dim_customer:Mapped["DimCustomerMySQL"] = relationship(back_populates="fact_order")
    dim_region:Mapped["DimRegionMySQL"] = relationship(back_populates="fact_order")
    dim_date:Mapped["DimDateMySQL"] = relationship(back_populates="fact_order")




class DimProductMySQL(Base):

    __tablename__ = "dim_product"

    product_id:Mapped[str] = mapped_column(String(20),primary_key=True)
    product_name:Mapped[str] = mapped_column(String(200))
    category:Mapped[str] = mapped_column(String(50))
    brand:Mapped[str] = mapped_column(String(50))

    fact_order:Mapped["FactOrderMySQL"] = relationship(back_populates="dim_product")




class DimCustomerMySQL(Base):

    __tablename__ = "dim_customer"

    customer_id:Mapped[str] = mapped_column(String(20),primary_key=True)
    customer_name:Mapped[str] = mapped_column(String(50))
    gender:Mapped[str] = mapped_column(String(10))
    member_level:Mapped[str] = mapped_column(String(20))

    fact_order: Mapped["FactOrderMySQL"] = relationship(back_populates="dim_customer")


class DimRegionMySQL(Base):

    __tablename__ = "dim_region"

    region_id:Mapped[str] = mapped_column(String(20),primary_key=True)
    province:Mapped[str] = mapped_column(String(50))
    region_name:Mapped[str] = mapped_column(String(50))
    country:Mapped[str] = mapped_column(String(50))

    fact_order: Mapped["FactOrderMySQL"] = relationship(back_populates="dim_region")


class DimDateMySQL(Base):

    __tablename__ = "dim_date"

    date_id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    year:Mapped[int] = mapped_column(Integer)
    quarter:Mapped[str] = mapped_column(String(2))
    month:Mapped[int] = mapped_column(Integer)
    day:Mapped[int] = mapped_column(Integer)

    fact_order: Mapped["FactOrderMySQL"] = relationship(back_populates="dim_date")






















