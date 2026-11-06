from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Application, Stage
from app.schemas import ApplicationCreate, ApplicationRead, ApplicationUpdate


def get_application_or_404(app_id: int, db: Session = Depends(get_db)) -> Application:
    obj = db.get(Application, app_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return obj


router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", response_model=ApplicationRead, status_code=201)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    obj = Application(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("", response_model=list[ApplicationRead], status_code=200)
def list_applications(
    stage: Stage | None = None,
    due_before: date | None = None,
    q: str | None = None,
    db: Session = Depends(get_db),
):
    stmt = select(Application).order_by(Application.created_at.desc())
    if stage is not None:  # filter
        stmt = stmt.where(Application.stage == stage)
    if due_before is not None:  # filter
        stmt = stmt.where(Application.follow_up_date <= due_before)
    if q:  # search
        like = f"%{q}%"
        stmt = stmt.where(
            or_(
                Application.company.ilike(like),
                Application.role.ilike(like),
                Application.notes.ilike(like),
            )
        )
    return db.scalars(stmt).all()


@router.get("/{app_id}", response_model=ApplicationRead)
def get_application(obj: Application = Depends(get_application_or_404)):
    return obj


@router.patch("/{app_id}", response_model=ApplicationRead)
def update_application(
    payload: ApplicationUpdate,
    obj: Application = Depends(get_application_or_404),
    db: Session = Depends(get_db),
):
    data = payload.model_dump(
        exclude_unset=True
    )  # only the fields the client actually sent
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{app_id}", status_code=204)
def delete_application(
    obj: Application = Depends(get_application_or_404),
    db: Session = Depends(get_db),
):
    db.delete(obj)
    db.commit()
