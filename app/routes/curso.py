from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models.curso import (
    Curso,
    CursoCreate,
    CursoRead,
    CursoUpdate
)

router = APIRouter(prefix="/cursos", tags=["cursos"])


@router.post("/", response_model=CursoRead, status_code=status.HTTP_201_CREATED)
def create_curso(
    curso: CursoCreate,
    session: Session = Depends(get_session)
):
    """Create a new curso"""
    db_curso = Curso.model_validate(curso)
    session.add(db_curso)
    session.commit()
    session.refresh(db_curso)
    return db_curso


@router.get("/", response_model=List[CursoRead])
def get_cursos(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Get all cursos"""
    cursos = session.exec(
        select(Curso).offset(skip).limit(limit)
    ).all()
    return cursos


@router.get("/{curso_id}", response_model=CursoRead)
def get_curso(
    curso_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific curso by ID"""
    curso = session.get(Curso, curso_id)
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso not found"
        )
    return curso


@router.patch("/{curso_id}", response_model=CursoRead)
def update_curso(
    curso_id: int,
    curso_update: CursoUpdate,
    session: Session = Depends(get_session)
):
    """Update a curso"""
    db_curso = session.get(Curso, curso_id)
    if not db_curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso not found"
        )

    curso_data = curso_update.model_dump(exclude_unset=True)
    for key, value in curso_data.items():
        setattr(db_curso, key, value)

    session.add(db_curso)
    session.commit()
    session.refresh(db_curso)
    return db_curso


@router.delete("/{curso_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_curso(
    curso_id: int,
    session: Session = Depends(get_session)
):
    """Delete a curso"""
    curso = session.get(Curso, curso_id)
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso not found"
        )

    session.delete(curso)
    session.commit()
    return None
