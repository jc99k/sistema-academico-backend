from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class PrerequisitoBase(SQLModel):
    """Base model for Prerrequisito"""
    curso_id: int = Field(foreign_key="curso.curso_id")
    curso_req_id: int = Field(foreign_key="curso.curso_id")


class Prerrequisito(PrerequisitoBase, table=True):
    """Prerrequisito table model"""
    prerrequisito_id: Optional[int] = Field(default=None, primary_key=True)
    fecha_registro: datetime = Field(default_factory=datetime.now)


class PrerequisitoCreate(PrerequisitoBase):
    """Schema for creating a new Prerrequisito"""
    pass


class PrerequisitoRead(PrerequisitoBase):
    """Schema for reading a Prerrequisito"""
    prerrequisito_id: int
    fecha_registro: datetime
