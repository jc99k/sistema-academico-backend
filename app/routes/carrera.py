from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models.carrera import (
    Carrera,
    CarreraCreate,
    CarreraRead,
    CarreraUpdate
)

router = APIRouter(prefix="/carreras", tags=["carreras"])


@router.post("/", response_model=CarreraRead, status_code=status.HTTP_201_CREATED)
def create_carrera(
    carrera: CarreraCreate,
    session: Session = Depends(get_session)
):
    """Create a new carrera"""
    db_carrera = Carrera.model_validate(carrera)
    session.add(db_carrera)
    session.commit()
    session.refresh(db_carrera)
    return db_carrera


@router.get("/", response_model=List[CarreraRead])
def get_carreras(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Get all carreras"""
    carreras = session.exec(
        select(Carrera).offset(skip).limit(limit)
    ).all()
    return carreras


@router.get("/{carrera_id}", response_model=CarreraRead)
def get_carrera(
    carrera_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific carrera by ID"""
    carrera = session.get(Carrera, carrera_id)
    if not carrera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carrera not found"
        )
    return carrera


@router.patch("/{carrera_id}", response_model=CarreraRead)
def update_carrera(
    carrera_id: int,
    carrera_update: CarreraUpdate,
    session: Session = Depends(get_session)
):
    """Update a carrera"""
    db_carrera = session.get(Carrera, carrera_id)
    if not db_carrera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carrera not found"
        )

    carrera_data = carrera_update.model_dump(exclude_unset=True)
    for key, value in carrera_data.items():
        setattr(db_carrera, key, value)

    session.add(db_carrera)
    session.commit()
    session.refresh(db_carrera)
    return db_carrera


@router.delete("/{carrera_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_carrera(
    carrera_id: int,
    session: Session = Depends(get_session)
):
    """Delete a carrera"""
    carrera = session.get(Carrera, carrera_id)
    if not carrera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carrera not found"
        )

    session.delete(carrera)
    session.commit()
    return None
