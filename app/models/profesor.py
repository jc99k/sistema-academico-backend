from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class ProfesorBase(SQLModel):
    """Base model for Profesor"""
    nombre: str = Field(max_length=50)
    apellido: str = Field(max_length=50)
    dni: str = Field(unique=True, max_length=20)
    email: str = Field(unique=True, max_length=100)
    telefono: Optional[str] = Field(default=None, max_length=20)
    especialidad: Optional[str] = Field(default=None, max_length=100)
    titulo_academico: Optional[str] = Field(default=None, max_length=100)
    activo: bool = Field(default=True)


class Profesor(ProfesorBase, table=True):
    """Profesor table model"""
    profesor_id: Optional[int] = Field(default=None, primary_key=True)
    fecha_registro: datetime = Field(default_factory=datetime.now)


class ProfesorCreate(ProfesorBase):
    """Schema for creating a new Profesor"""
    pass


class ProfesorUpdate(SQLModel):
    """Schema for updating a Profesor"""
    nombre: Optional[str] = Field(default=None, max_length=50)
    apellido: Optional[str] = Field(default=None, max_length=50)
    dni: Optional[str] = Field(default=None, max_length=20)
    email: Optional[str] = Field(default=None, max_length=100)
    telefono: Optional[str] = Field(default=None, max_length=20)
    especialidad: Optional[str] = Field(default=None, max_length=100)
    titulo_academico: Optional[str] = Field(default=None, max_length=100)
    activo: Optional[bool] = None


class ProfesorRead(ProfesorBase):
    """Schema for reading a Profesor"""
    profesor_id: int
    fecha_registro: datetime
