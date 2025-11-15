from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models.facultad import (
    Facultad,
    FacultadCreate,
    FacultadRead,
    FacultadUpdate
)

router = APIRouter(prefix="/facultades", tags=["facultades"])


@router.post("/", response_model=FacultadRead, status_code=status.HTTP_201_CREATED)
def create_facultad(
    facultad: FacultadCreate,
    session: Session = Depends(get_session)
):
    """Create a new facultad"""
    db_facultad = Facultad.model_validate(facultad)
    session.add(db_facultad)
    session.commit()
    session.refresh(db_facultad)
    return db_facultad


@router.get("/", response_model=List[FacultadRead])
def get_facultades(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Get all facultades"""
    facultades = session.exec(
        select(Facultad).offset(skip).limit(limit)
    ).all()
    return facultades


@router.get("/{facultad_id}", response_model=FacultadRead)
def get_facultad(
    facultad_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific facultad by ID"""
    facultad = session.get(Facultad, facultad_id)
    if not facultad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Facultad not found"
        )
    return facultad


@router.patch("/{facultad_id}", response_model=FacultadRead)
def update_facultad(
    facultad_id: int,
    facultad_update: FacultadUpdate,
    session: Session = Depends(get_session)
):
    """Update a facultad"""
    db_facultad = session.get(Facultad, facultad_id)
    if not db_facultad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Facultad not found"
        )

    facultad_data = facultad_update.model_dump(exclude_unset=True)
    for key, value in facultad_data.items():
        setattr(db_facultad, key, value)

    session.add(db_facultad)
    session.commit()
    session.refresh(db_facultad)
    return db_facultad


@router.delete("/{facultad_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_facultad(
    facultad_id: int,
    session: Session = Depends(get_session)
):
    """Delete a facultad"""
    facultad = session.get(Facultad, facultad_id)
    if not facultad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Facultad not found"
        )

    session.delete(facultad)
    session.commit()
    return None
