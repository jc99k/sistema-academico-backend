from datetime import datetime
from typing import Optional
from decimal import Decimal
from sqlmodel import Field, SQLModel


class CalificacionBase(SQLModel):
    """Base model for Calificacion"""
    matricula_id: int = Field(foreign_key="matricula.matricula_id", unique=True)
    nota: Optional[Decimal] = Field(default=None, ge=0, le=20, decimal_places=2)
    observacion: Optional[str] = None


class Calificacion(CalificacionBase, table=True):
    """Calificacion table model"""
    calificacion_id: Optional[int] = Field(default=None, primary_key=True)
    fecha_registro: datetime = Field(default_factory=datetime.now)


class CalificacionCreate(CalificacionBase):
    """Schema for creating a new Calificacion"""
    pass


class CalificacionUpdate(SQLModel):
    """Schema for updating a Calificacion"""
    nota: Optional[Decimal] = Field(default=None, ge=0, le=20, decimal_places=2)
    observacion: Optional[str] = None


class CalificacionRead(CalificacionBase):
    """Schema for reading a Calificacion"""
    calificacion_id: int
    fecha_registro: datetime
