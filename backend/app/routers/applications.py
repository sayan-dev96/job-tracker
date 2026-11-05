from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Application
from app.schemas import ApplicationCreate, ApplicationRead

router = APIRouter(prefix='/applications', tags=['applications'])

@router.post('', response_model=ApplicationRead, status_code=201)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    obj = Application(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get('', response_model=list[ApplicationRead], status_code=200)
def list_applications(db: Session = Depends(get_db)):
    rows = db.scalars(select(Application).order_by(Application.created_at.desc())).all()
    return rows

from fastapi import HTTPException

def get_application_or_404(app_id: int, db: Session = Depends(get_db)) -> Application:
    obj = db.get(Application, app_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return obj

@router.get("/{app_id}", response_model=ApplicationRead)
def get_application(obj: Application = Depends(get_application_or_404)):
    return obj