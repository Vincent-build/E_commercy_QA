from app.operated_database.mysql.orm.meta_db_model.base_model import Base
from sqlalchemy import String,Text,JSON
from sqlalchemy.orm import Mapped,mapped_column

class MetricInfoMySQL(Base):
    __tablename__ = "metric_info"

    id:Mapped[str] = mapped_column(String(64),primary_key=True,comment="指标编码")
    name:Mapped[str] = mapped_column(String(128),comment="指标名称")
    description:Mapped[str] = mapped_column(Text,comment="指标描述")
    relevant_columns:Mapped[dict|list|None] = mapped_column(JSON,comment="关联字段")
    alias:Mapped[dict|list|None] = mapped_column(JSON,comment="指标别名")

