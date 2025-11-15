from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models.calificacion import (
    Calificacion,
    CalificacionCreate,
    CalificacionRead,
    CalificacionUpdate
)

router = APIRouter(prefix="/calificaciones", tags=["calificaciones"])


@router.post("/", response_model=CalificacionRead, status_code=status.HTTP_201_CREATED)
def create_calificacion(
    calificacion: CalificacionCreate,
    session: Session = Depends(get_session)
):
    """Create a new calificacion"""
    db_calificacion = Calificacion.model_validate(calificacion)
    session.add(db_calificacion)
    session.commit()
    session.refresh(db_calificacion)
    return db_calificacion


@router.get("/", response_model=List[CalificacionRead])
def get_calificaciones(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Get all calificaciones"""
    calificaciones = session.exec(
        select(Calificacion).offset(skip).limit(limit)
    ).all()
    return calificaciones


@router.get("/{calificacion_id}", response_model=CalificacionRead)
def get_calificacion(
    calificacion_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific calificacion by ID"""
    calificacion = session.get(Calificacion, calificacion_id)
    if not calificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calificacion not found"
        )
    return calificacion


@router.patch("/{calificacion_id}", response_model=CalificacionRead)
def update_calificacion(
    calificacion_id: int,
    calificacion_update: CalificacionUpdate,
    session: Session = Depends(get_session)
):
    """Update a calificacion"""
    db_calificacion = session.get(Calificacion, calificacion_id)
    if not db_calificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calificacion not found"
        )

    calificacion_data = calificacion_update.model_dump(exclude_unset=True)
    for key, value in calificacion_data.items():
        setattr(db_calificacion, key, value)

    session.add(db_calificacion)
    session.commit()
    session.refresh(db_calificacion)
    return db_calificacion


@router.delete("/{calificacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calificacion(
    calificacion_id: int,
    session: Session = Depends(get_session)
):
    """Delete a calificacion"""
    calificacion = session.get(Calificacion, calificacion_id)
    if not calificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calificacion not found"
        )

    session.delete(calificacion)
    session.commit()
    return None
