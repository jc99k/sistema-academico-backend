from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models.matricula import (
    Matricula,
    MatriculaCreate,
    MatriculaRead,
    MatriculaUpdate
)

router = APIRouter(prefix="/matriculas", tags=["matriculas"])


@router.post("/", response_model=MatriculaRead, status_code=status.HTTP_201_CREATED)
def create_matricula(
    matricula: MatriculaCreate,
    session: Session = Depends(get_session)
):
    """Create a new matricula"""
    db_matricula = Matricula.model_validate(matricula)
    session.add(db_matricula)
    session.commit()
    session.refresh(db_matricula)
    return db_matricula


@router.get("/", response_model=List[MatriculaRead])
def get_matriculas(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Get all matriculas"""
    matriculas = session.exec(
        select(Matricula).offset(skip).limit(limit)
    ).all()
    return matriculas


@router.get("/{matricula_id}", response_model=MatriculaRead)
def get_matricula(
    matricula_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific matricula by ID"""
    matricula = session.get(Matricula, matricula_id)
    if not matricula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matricula not found"
        )
    return matricula


@router.patch("/{matricula_id}", response_model=MatriculaRead)
def update_matricula(
    matricula_id: int,
    matricula_update: MatriculaUpdate,
    session: Session = Depends(get_session)
):
    """Update a matricula"""
    db_matricula = session.get(Matricula, matricula_id)
    if not db_matricula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matricula not found"
        )

    matricula_data = matricula_update.model_dump(exclude_unset=True)
    for key, value in matricula_data.items():
        setattr(db_matricula, key, value)

    session.add(db_matricula)
    session.commit()
    session.refresh(db_matricula)
    return db_matricula


@router.delete("/{matricula_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_matricula(
    matricula_id: int,
    session: Session = Depends(get_session)
):
    """Delete a matricula"""
    matricula = session.get(Matricula, matricula_id)
    if not matricula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matricula not found"
        )

    session.delete(matricula)
    session.commit()
    return None
