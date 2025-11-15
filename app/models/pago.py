from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from sqlmodel import Field, SQLModel


class PagoBase(SQLModel):
    """Base model for Pago"""
    matricula_id: int = Field(foreign_key="matricula.matricula_id")
    fecha_pago: date = Field(default_factory=date.today)
    monto: Decimal = Field(gt=0, decimal_places=2)
    metodo_pago: str = Field(max_length=50)
    referencia: Optional[str] = Field(default=None, max_length=100)
    estado: str = Field(default="PROCESADO", max_length=20)


class Pago(PagoBase, table=True):
    """Pago table model"""
    pago_id: Optional[int] = Field(default=None, primary_key=True)
    fecha_registro: datetime = Field(default_factory=datetime.now)


class PagoCreate(PagoBase):
    """Schema for creating a new Pago"""
    pass


class PagoUpdate(SQLModel):
    """Schema for updating a Pago"""
    estado: Optional[str] = Field(default=None, max_length=20)
    referencia: Optional[str] = Field(default=None, max_length=100)


class PagoRead(PagoBase):
    """Schema for reading a Pago"""
    pago_id: int
    fecha_registro: datetime
