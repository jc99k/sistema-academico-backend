from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models.seccion import (
    Seccion,
    SeccionCreate,
    SeccionRead,
    SeccionUpdate
)

router = APIRouter(prefix="/secciones", tags=["secciones"])


@router.post("/", response_model=SeccionRead, status_code=status.HTTP_201_CREATED)
def create_seccion(
    seccion: SeccionCreate,
    session: Session = Depends(get_session)
):
    """Create a new seccion"""
    db_seccion = Seccion.model_validate(seccion)
    session.add(db_seccion)
    session.commit()
    session.refresh(db_seccion)
    return db_seccion


@router.get("/", response_model=List[SeccionRead])
def get_secciones(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Get all secciones"""
    secciones = session.exec(
        select(Seccion).offset(skip).limit(limit)
    ).all()
    return secciones


@router.get("/{seccion_id}", response_model=SeccionRead)
def get_seccion(
    seccion_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific seccion by ID"""
    seccion = session.get(Seccion, seccion_id)
    if not seccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seccion not found"
        )
    return seccion


@router.patch("/{seccion_id}", response_model=SeccionRead)
def update_seccion(
    seccion_id: int,
    seccion_update: SeccionUpdate,
    session: Session = Depends(get_session)
):
    """Update a seccion"""
    db_seccion = session.get(Seccion, seccion_id)
    if not db_seccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seccion not found"
        )

    seccion_data = seccion_update.model_dump(exclude_unset=True)
    for key, value in seccion_data.items():
        setattr(db_seccion, key, value)

    session.add(db_seccion)
    session.commit()
    session.refresh(db_seccion)
    return db_seccion


@router.delete("/{seccion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_seccion(
    seccion_id: int,
    session: Session = Depends(get_session)
):
    """Delete a seccion"""
    seccion = session.get(Seccion, seccion_id)
    if not seccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seccion not found"
        )

    session.delete(seccion)
    session.commit()
    return None
