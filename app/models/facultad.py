from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class FacultadBase(SQLModel):
    """Base model for Facultad"""
    nombre: str = Field(unique=True, max_length=100)
    descripcion: Optional[str] = None
    ubicacion: Optional[str] = Field(default=None, max_length=100)
    decano: Optional[str] = Field(default=None, max_length=100)
    activo: bool = Field(default=True)


class Facultad(FacultadBase, table=True):
    """Facultad table model"""
    facultad_id: Optional[int] = Field(default=None, primary_key=True)
    fecha_registro: datetime = Field(default_factory=datetime.now)


class FacultadCreate(FacultadBase):
    """Schema for creating a new Facultad"""
    pass


class FacultadUpdate(SQLModel):
    """Schema for updating a Facultad"""
    nombre: Optional[str] = Field(default=None, max_length=100)
    descripcion: Optional[str] = None
    ubicacion: Optional[str] = Field(default=None, max_length=100)
    decano: Optional[str] = Field(default=None, max_length=100)
    activo: Optional[bool] = None


class FacultadRead(FacultadBase):
    """Schema for reading a Facultad"""
    facultad_id: int
    fecha_registro: datetime
