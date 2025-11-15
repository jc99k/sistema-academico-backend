from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class CursoBase(SQLModel):
    """Base model for Curso"""
    carrera_id: int = Field(foreign_key="carrera.carrera_id")
    codigo: str = Field(unique=True, max_length=20)
    nombre: str = Field(max_length=100)
    descripcion: Optional[str] = None
    creditos: int = Field(gt=0)
    nivel_semestre: int = Field(gt=0)
    activo: bool = Field(default=True)


class Curso(CursoBase, table=True):
    """Curso table model"""
    curso_id: Optional[int] = Field(default=None, primary_key=True)
    fecha_registro: datetime = Field(default_factory=datetime.now)


class CursoCreate(CursoBase):
    """Schema for creating a new Curso"""
    pass


class CursoUpdate(SQLModel):
    """Schema for updating a Curso"""
    carrera_id: Optional[int] = None
    codigo: Optional[str] = Field(default=None, max_length=20)
    nombre: Optional[str] = Field(default=None, max_length=100)
    descripcion: Optional[str] = None
    creditos: Optional[int] = Field(default=None, gt=0)
    nivel_semestre: Optional[int] = Field(default=None, gt=0)
    activo: Optional[bool] = None


class CursoRead(CursoBase):
    """Schema for reading a Curso"""
    curso_id: int
    fecha_registro: datetime
