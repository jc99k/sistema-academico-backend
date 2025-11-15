from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models.pago import (
    Pago,
    PagoCreate,
    PagoRead,
    PagoUpdate
)

router = APIRouter(prefix="/pagos", tags=["pagos"])


@router.post("/", response_model=PagoRead, status_code=status.HTTP_201_CREATED)
def create_pago(
    pago: PagoCreate,
    session: Session = Depends(get_session)
):
    """Create a new pago"""
    db_pago = Pago.model_validate(pago)
    session.add(db_pago)
    session.commit()
    session.refresh(db_pago)
    return db_pago


@router.get("/", response_model=List[PagoRead])
def get_pagos(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Get all pagos"""
    pagos = session.exec(
        select(Pago).offset(skip).limit(limit)
    ).all()
    return pagos


@router.get("/{pago_id}", response_model=PagoRead)
def get_pago(
    pago_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific pago by ID"""
    pago = session.get(Pago, pago_id)
    if not pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago not found"
        )
    return pago


@router.patch("/{pago_id}", response_model=PagoRead)
def update_pago(
    pago_id: int,
    pago_update: PagoUpdate,
    session: Session = Depends(get_session)
):
    """Update a pago"""
    db_pago = session.get(Pago, pago_id)
    if not db_pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago not found"
        )

    pago_data = pago_update.model_dump(exclude_unset=True)
    for key, value in pago_data.items():
        setattr(db_pago, key, value)

    session.add(db_pago)
    session.commit()
    session.refresh(db_pago)
    return db_pago


@router.delete("/{pago_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pago(
    pago_id: int,
    session: Session = Depends(get_session)
):
    """Delete a pago"""
    pago = session.get(Pago, pago_id)
    if not pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago not found"
        )

    session.delete(pago)
    session.commit()
    return None
