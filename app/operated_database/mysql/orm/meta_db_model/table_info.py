from app.operated_database.mysql.orm.meta_db_model.base_model import Base
from sqlalchemy import String,Text
from sqlalchemy.orm import Mapped,mapped_column


class TableInfoMySQL(Base):
    __tablename__ = "table_info"

    id:Mapped[str] = mapped_column(String(64),primary_key=True,comment="表编号")
    name:Mapped[str] = mapped_column(String(128),comment="表名称")
    role:Mapped[str] = mapped_column(String(32),comment="表类型")
    description:Mapped[str] = mapped_column(Text,comment="表描述")

