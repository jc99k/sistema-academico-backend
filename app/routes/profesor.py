from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models.profesor import (
    Profesor,
    ProfesorCreate,
    ProfesorRead,
    ProfesorUpdate
)

router = APIRouter(prefix="/profesores", tags=["profesores"])


@router.post("/", response_model=ProfesorRead, status_code=status.HTTP_201_CREATED)
def create_profesor(
    profesor: ProfesorCreate,
    session: Session = Depends(get_session)
):
    """Create a new profesor"""
    db_profesor = Profesor.model_validate(profesor)
    session.add(db_profesor)
    session.commit()
    session.refresh(db_profesor)
    return db_profesor


@router.get("/", response_model=List[ProfesorRead])
def get_profesores(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Get all profesores"""
    profesores = session.exec(
        select(Profesor).offset(skip).limit(limit)
    ).all()
    return profesores


@router.get("/{profesor_id}", response_model=ProfesorRead)
def get_profesor(
    profesor_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific profesor by ID"""
    profesor = session.get(Profesor, profesor_id)
    if not profesor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesor not found"
        )
    return profesor


@router.patch("/{profesor_id}", response_model=ProfesorRead)
def update_profesor(
    profesor_id: int,
    profesor_update: ProfesorUpdate,
    session: Session = Depends(get_session)
):
    """Update a profesor"""
    db_profesor = session.get(Profesor, profesor_id)
    if not db_profesor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesor not found"
        )

    profesor_data = profesor_update.model_dump(exclude_unset=True)
    for key, value in profesor_data.items():
        setattr(db_profesor, key, value)

    session.add(db_profesor)
    session.commit()
    session.refresh(db_profesor)
    return db_profesor


@router.delete("/{profesor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profesor(
    profesor_id: int,
    session: Session = Depends(get_session)
):
    """Delete a profesor"""
    profesor = session.get(Profesor, profesor_id)
    if not profesor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesor not found"
        )

    session.delete(profesor)
    session.commit()
    return None
