from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models.estudiante import (
    Estudiante,
    EstudianteCreate,
    EstudianteRead,
    EstudianteUpdate
)

router = APIRouter(prefix="/estudiantes", tags=["estudiantes"])


@router.post("/", response_model=EstudianteRead, status_code=status.HTTP_201_CREATED)
def create_estudiante(
    estudiante: EstudianteCreate,
    session: Session = Depends(get_session)
):
    """Create a new estudiante"""
    db_estudiante = Estudiante.model_validate(estudiante)
    session.add(db_estudiante)
    session.commit()
    session.refresh(db_estudiante)
    return db_estudiante


@router.get("/", response_model=List[EstudianteRead])
def get_estudiantes(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Get all estudiantes"""
    estudiantes = session.exec(
        select(Estudiante).offset(skip).limit(limit)
    ).all()
    return estudiantes


@router.get("/{estudiante_id}", response_model=EstudianteRead)
def get_estudiante(
    estudiante_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific estudiante by ID"""
    estudiante = session.get(Estudiante, estudiante_id)
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante not found"
        )
    return estudiante


@router.patch("/{estudiante_id}", response_model=EstudianteRead)
def update_estudiante(
    estudiante_id: int,
    estudiante_update: EstudianteUpdate,
    session: Session = Depends(get_session)
):
    """Update an estudiante"""
    db_estudiante = session.get(Estudiante, estudiante_id)
    if not db_estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante not found"
        )

    estudiante_data = estudiante_update.model_dump(exclude_unset=True)
    for key, value in estudiante_data.items():
        setattr(db_estudiante, key, value)

    session.add(db_estudiante)
    session.commit()
    session.refresh(db_estudiante)
    return db_estudiante


@router.delete("/{estudiante_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_estudiante(
    estudiante_id: int,
    session: Session = Depends(get_session)
):
    """Delete an estudiante"""
    estudiante = session.get(Estudiante, estudiante_id)
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estudiante not found"
        )

    session.delete(estudiante)
    session.commit()
    return None
