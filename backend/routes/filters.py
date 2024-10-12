from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db

router = APIRouter()

@router.get("/filter_symptoms_by_age/")
def filter_symptoms_by_age(start_date: str, end_date: str, age_group: str, db: Session = Depends(get_db)):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    age_range = [int(i) for i in age_group.split('-')]

    results = (
        db.query(
            models.Symptom.symptom_name,
            func.avg(models.Symptom.severity).label("average_severity"),
            func.count(models.Tag.tag_name).label("trigger_count")
        )
        .join(models.CheckIn, models.Symptom.checkin_id == models.CheckIn.checkin_id)
        .join(models.User, models.CheckIn.user_id == models.User.user_id)
        .join(models.Tag, models.CheckIn.checkin_id == models.Tag.checkin_id)
        .filter(
            models.User.age >= age_range[0],
            models.User.age <= age_range[1],
            models.CheckIn.checkin_date.between(start_date, end_date)
        )
        .group_by(models.Symptom.symptom_name)
        .all()
    )
    return results

@router.get("/trigger_impact/")
def get_trigger_impact(trigger: str, period: int, db: Session = Depends(get_db)):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30 * period)

    results = (
        db.query(
            models.Symptom.symptom_name,
            models.Symptom.severity,
            models.Tag.tag_name
        )
        .join(models.CheckIn, models.Symptom.checkin_id == models.CheckIn.checkin_id)
        .join(models.Tag, models.CheckIn.checkin_id == models.Tag.checkin_id)
        .filter(
            models.Tag.tag_name == trigger,
            models.CheckIn.checkin_date.between(start_date, end_date)
        )
        .all()
    )
    return results
