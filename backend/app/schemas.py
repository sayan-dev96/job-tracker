from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from app.models import Stage


class ApplicationCreate(BaseModel):
    company: str
    notes: str | None = None
    role: str
    url: str | None = None
    stage: Stage = Stage.APPLIED
    contact_name: str | None = None
    contact_email: EmailStr | None = None
    follow_up_date: date | None = None


class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    role: str
    stage: Stage
    notes: str | None
    url: str | None
    contact_name: str | None
    contact_email: str | None
    follow_up_date: date | None
    created_at: datetime
    updated_at: datetime


class ApplicationUpdate(BaseModel):
    company: str | None = None
    notes: str | None = None
    role: str | None = None
    url: str | None = None
    stage: Stage | None = None
    contact_name: str | None = None
    contact_email: EmailStr | None = None
    follow_up_date: date | None = None

    @field_validator("company", "role", "stage")
    @classmethod
    def not_null(cls, v):
        if v is None:
            raise ValueError("cannot be null")
        return v
