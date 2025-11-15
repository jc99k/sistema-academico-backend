from datetime import datetime, date
from typing import Optional
from sqlmodel import Field, SQLModel


class EstudianteBase(SQLModel):
    """Base model for Estudiante"""
    nombre: str = Field(max_length=50)
    apellido: str = Field(max_length=50)
    dni: str = Field(unique=True, max_length=20)
    email: str = Field(unique=True, max_length=100)
    telefono: Optional[str] = Field(default=None, max_length=20)
    fecha_nacimiento: date
    direccion: Optional[str] = Field(default=None, max_length=200)
    activo: bool = Field(default=True)


class Estudiante(EstudianteBase, table=True):
    """Estudiante table model"""
    estudiante_id: Optional[int] = Field(default=None, primary_key=True)
    fecha_registro: datetime = Field(default_factory=datetime.now)


class EstudianteCreate(EstudianteBase):
    """Schema for creating a new Estudiante"""
    pass


class EstudianteUpdate(SQLModel):
    """Schema for updating an Estudiante"""
    nombre: Optional[str] = Field(default=None, max_length=50)
    apellido: Optional[str] = Field(default=None, max_length=50)
    dni: Optional[str] = Field(default=None, max_length=20)
    email: Optional[str] = Field(default=None, max_length=100)
    telefono: Optional[str] = Field(default=None, max_length=20)
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = Field(default=None, max_length=200)
    activo: Optional[bool] = None


class EstudianteRead(EstudianteBase):
    """Schema for reading an Estudiante"""
    estudiante_id: int
    fecha_registro: datetime
