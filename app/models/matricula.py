from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from sqlmodel import Field, SQLModel


class MatriculaBase(SQLModel):
    """Base model for Matricula"""
    estudiante_id: int = Field(foreign_key="estudiante.estudiante_id")
    seccion_id: int = Field(foreign_key="seccion.seccion_id")
    fecha_matricula: date = Field(default_factory=date.today)
    estado: str = Field(default="PENDIENTE", max_length=20)
    costo: Decimal = Field(ge=0, decimal_places=2)
    metodo_pago: Optional[str] = Field(default=None, max_length=50)


class Matricula(MatriculaBase, table=True):
    """Matricula table model"""
    matricula_id: Optional[int] = Field(default=None, primary_key=True)
    fecha_registro: datetime = Field(default_factory=datetime.now)


class MatriculaCreate(MatriculaBase):
    """Schema for creating a new Matricula"""
    pass


class MatriculaUpdate(SQLModel):
    """Schema for updating a Matricula"""
    estado: Optional[str] = Field(default=None, max_length=20)
    costo: Optional[Decimal] = Field(default=None, ge=0, decimal_places=2)
    metodo_pago: Optional[str] = Field(default=None, max_length=50)


class MatriculaRead(MatriculaBase):
    """Schema for reading a Matricula"""
    matricula_id: int
    fecha_registro: datetime
