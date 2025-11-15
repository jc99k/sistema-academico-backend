from datetime import datetime, date
from typing import Optional
from sqlmodel import Field, SQLModel


class SeccionBase(SQLModel):
    """Base model for Seccion"""
    curso_id: int = Field(foreign_key="curso.curso_id")
    profesor_id: int = Field(foreign_key="profesor.profesor_id")
    codigo: str = Field(max_length=20)
    capacidad_maxima: int = Field(gt=0)
    aula: Optional[str] = Field(default=None, max_length=50)
    horario: Optional[str] = Field(default=None, max_length=50)
    dias: Optional[str] = Field(default=None, max_length=50)
    periodo_academico: str = Field(max_length=20)
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    activo: bool = Field(default=True)


class Seccion(SeccionBase, table=True):
    """Seccion table model"""
    seccion_id: Optional[int] = Field(default=None, primary_key=True)
    fecha_registro: datetime = Field(default_factory=datetime.now)


class SeccionCreate(SeccionBase):
    """Schema for creating a new Seccion"""
    pass


class SeccionUpdate(SQLModel):
    """Schema for updating a Seccion"""
    curso_id: Optional[int] = None
    profesor_id: Optional[int] = None
    codigo: Optional[str] = Field(default=None, max_length=20)
    capacidad_maxima: Optional[int] = Field(default=None, gt=0)
    aula: Optional[str] = Field(default=None, max_length=50)
    horario: Optional[str] = Field(default=None, max_length=50)
    dias: Optional[str] = Field(default=None, max_length=50)
    periodo_academico: Optional[str] = Field(default=None, max_length=20)
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    activo: Optional[bool] = None


class SeccionRead(SeccionBase):
    """Schema for reading a Seccion"""
    seccion_id: int
    fecha_registro: datetime
