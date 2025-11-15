from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class CarreraBase(SQLModel):
    """Base model for Carrera"""
    facultad_id: int = Field(foreign_key="facultad.facultad_id")
    nombre: str = Field(unique=True, max_length=100)
    descripcion: Optional[str] = None
    duracion_semestres: int
    titulo_otorgado: Optional[str] = Field(default=None, max_length=100)
    activo: bool = Field(default=True)


class Carrera(CarreraBase, table=True):
    """Carrera table model"""
    carrera_id: Optional[int] = Field(default=None, primary_key=True)
    fecha_registro: datetime = Field(default_factory=datetime.now)


class CarreraCreate(CarreraBase):
    """Schema for creating a new Carrera"""
    pass


class CarreraUpdate(SQLModel):
    """Schema for updating a Carrera"""
    facultad_id: Optional[int] = None
    nombre: Optional[str] = Field(default=None, max_length=100)
    descripcion: Optional[str] = None
    duracion_semestres: Optional[int] = None
    titulo_otorgado: Optional[str] = Field(default=None, max_length=100)
    activo: Optional[bool] = None


class CarreraRead(CarreraBase):
    """Schema for reading a Carrera"""
    carrera_id: int
    fecha_registro: datetime
