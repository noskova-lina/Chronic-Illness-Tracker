from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
import pandas as pd
from backend.database import engine, get_db
from backend import models, schemas

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Read the CSV file
    df = pd.read_csv(file.file, delimiter=',', low_memory=False)

    try:
        # Insert data into the database
        for _, row in df.iterrows():
            # Insert User if not exists
            user_id = row['user_id']
            existing_user = db.query(models.User).filter(models.User.user_id == user_id).first()

            if not existing_user:
                user = models.User(
                    user_id=user_id,
                    age=row['age'] if pd.notnull(row['age']) else None,
                    sex=row['sex'] if pd.notnull(row['sex']) else None,
                    country=row['country'] if pd.notnull(row['country']) else None
                )
                db.add(user)
                db.commit()
                db.refresh(user)

            # Parse check-in date with flexible format handling
            try:
                checkin_date = pd.to_datetime(row['checkin_date'], format='%d/%m/%Y', dayfirst=True)
            except ValueError:
                checkin_date = pd.to_datetime(row['checkin_date'], format='%Y-%m-%d')

            # Insert CheckIn if not exists
            existing_checkin = db.query(models.CheckIn).filter(models.CheckIn.user_id == user_id,
                                                               models.CheckIn.date == checkin_date).first()

            if not existing_checkin:
                checkin = models.CheckIn(
                    user_id=user_id,
                    date=checkin_date
                )
                db.add(checkin)
                db.commit()
                db.refresh(checkin)
            else:
                checkin = existing_checkin

            # Insert based on trackable_type
            trackable_type = row['trackable_type']

            if trackable_type in ['Condition', 'Symptom']:
                # Check if the symptom already exists for this check-in
                existing_symptom = db.query(models.Symptom).filter(models.Symptom.checkin_id == checkin.checkin_id,
                                                                   models.Symptom.symptom_name == row[
                                                                       'trackable_name']).first()

                if not existing_symptom:
                    symptom = models.Symptom(
                        checkin_id=checkin.checkin_id,
                        symptom_name=row['trackable_name'],
                        severity=int(row['trackable_value'])
                    )
                    db.add(symptom)
                    db.commit()

            elif trackable_type == 'Tag':
                # Check if the tag already exists for this check-in
                existing_tag = db.query(models.Tag).filter(models.Tag.checkin_id == checkin.checkin_id,
                                                           models.Tag.tag_name == row['trackable_name']).first()

                if not existing_tag:
                    tag = models.Tag(
                        checkin_id=checkin.checkin_id,
                        tag_name=row['trackable_name']
                    )
                    db.add(tag)
                    db.commit()

            elif trackable_type == 'Treatment':
                # Check if the treatment already exists for this check-in
                existing_treatment = db.query(models.Treatment).filter(
                    models.Treatment.checkin_id == checkin.checkin_id,
                    models.Treatment.treatment_name == row['trackable_name']).first()

                if not existing_treatment:
                    treatment = models.Treatment(
                        checkin_id=checkin.checkin_id,
                        treatment_name=row['trackable_name']
                    )
                    db.add(treatment)
                    db.commit()

            elif trackable_type == 'Weather':
                # Check if the weather entry already exists for this check-in
                existing_weather = db.query(models.Weather).filter(
                    models.Weather.checkin_id == checkin.checkin_id).first()

                if not existing_weather:
                    # Assuming weather data is comma-separated in 'trackable_value'
                    weather_data = row['trackable_value'].split(',')
                    weather = models.Weather(
                        checkin_id=checkin.checkin_id,
                        description=row['trackable_name'],
                        temperature=float(weather_data[0]) if weather_data[0] else None,
                        humidity=float(weather_data[1]) if len(weather_data) > 1 else None,
                        pressure=float(weather_data[2]) if len(weather_data) > 2 else None
                    )
                    db.add(weather)
                    db.commit()

        return {"message": "Data successfully inserted into the database."}

    except Exception as e:
        return {"error": str(e)}


# User endpoints
@app.get("/users", response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.post("/add_user", response_model=schemas.User)
def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# CheckIn endpoints
@app.get("/checkins", response_model=list[schemas.Checkin])
def get_checkins(db: Session = Depends(get_db)):
    checkins = db.query(models.CheckIn).all()
    return checkins


@app.post("/add_checkin", response_model=schemas.Checkin)
def add_checkin(checkin: schemas.CheckinCreate, db: Session = Depends(get_db)):
    db_checkin = models.CheckIn(**checkin.dict())
    db.add(db_checkin)
    db.commit()
    db.refresh(db_checkin)
    return db_checkin


# Symptom endpoints
@app.get("/symptoms", response_model=list[schemas.Symptom])
def get_symptoms(db: Session = Depends(get_db)):
    symptoms = db.query(models.Symptom).all()
    return symptoms


@app.post("/add_symptom", response_model=schemas.Symptom)
def add_symptom(symptom: schemas.SymptomCreate, db: Session = Depends(get_db)):
    db_symptom = models.Symptom(**symptom.dict())
    db.add(db_symptom)
    db.commit()
    db.refresh(db_symptom)
    return db_symptom


# Treatment endpoints
@app.get("/treatments", response_model=list[schemas.Treatment])
def get_treatments(db: Session = Depends(get_db)):
    treatments = db.query(models.Treatment).all()
    return treatments


@app.post("/add_treatment", response_model=schemas.Treatment)
def add_treatment(treatment: schemas.TreatmentCreate, db: Session = Depends(get_db)):
    db_treatment = models.Treatment(**treatment.dict())
    db.add(db_treatment)
    db.commit()
    db.refresh(db_treatment)
    return db_treatment


# Tag endpoints
@app.get("/tags", response_model=list[schemas.Tag])
def get_tags(db: Session = Depends(get_db)):
    tags = db.query(models.Tag).all()
    return tags


@app.post("/add_tag", response_model=schemas.Tag)
def add_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    db_tag = models.Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


# Weather endpoints
@app.get("/weather", response_model=list[schemas.Weather])
def get_weather(db: Session = Depends(get_db)):
    weather_records = db.query(models.Weather).all()
    return weather_records


@app.post("/add_weather", response_model=schemas.Weather)
def add_weather(weather: schemas.WeatherCreate, db: Session = Depends(get_db)):
    db_weather = models.Weather(**weather.dict())
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    return db_weather


@app.get("/average_symptom_severity/")
def get_average_symptom_severity(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.CheckIn.date,
            func.avg(models.Symptom.severity).label("average_severity")
        )
        .join(models.Symptom)
        .group_by(models.CheckIn.date)
        .order_by(models.CheckIn.date)
        .all()
    )

    average_severity_data = [{"date": result.date.strftime("%Y-%m-%d"), "average_severity": result.average_severity} for
                             result in results]

    return average_severity_data


@app.get("/treatment_frequency/")
def get_treatment_frequency(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Treatment.treatment_name,
            func.count(models.Treatment.treatment_id).label("frequency")
        )
        .group_by(models.Treatment.treatment_name)
        .order_by(func.count(models.Treatment.treatment_id).desc())
        .all()
    )

    frequency_data = [{"treatment_name": result.treatment_name, "frequency": result.frequency} for result in results]

    return frequency_data


@app.get("/trigger_impact/")
def get_trigger_impact(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Tag.tag_name,
            func.avg(models.Symptom.severity).label("average_severity")
        )
        .join(models.Tag, models.Tag.checkin_id == models.Symptom.checkin_id)
        .group_by(models.Tag.tag_name)
        .order_by(func.avg(models.Symptom.severity).desc())
        .all()
    )

    impact_data = [{"trigger": result.tag_name, "average_severity": result.average_severity} for result in results]

    return impact_data


@app.get("/symptoms_by_age_group/")
def get_symptoms_by_age_group(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.User.age,
            models.Symptom.symptom_name,
            func.avg(models.Symptom.severity).label("average_severity")
        )
        .select_from(models.CheckIn)
        .join(models.User, models.CheckIn.user_id == models.User.user_id)
        .join(models.Symptom, models.CheckIn.checkin_id == models.Symptom.checkin_id)
        .group_by(models.User.age, models.Symptom.symptom_name)
        .order_by(models.User.age)
        .all()
    )

    symptoms_by_age = [
        {"age": result.age, "symptom": result.symptom_name, "average_severity": result.average_severity}
        for result in results
    ]

    return symptoms_by_age


@app.get("/symptoms_by_period/")
def get_symptoms_by_period(start_date: str, end_date: str, db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Symptom.symptom_name,
            models.Symptom.severity,
            models.CheckIn.date
        )
        .join(models.CheckIn)
        .filter(models.CheckIn.date >= start_date, models.CheckIn.date <= end_date)
        .all()
    )

    symptoms_data = [
        {"symptom": result.symptom_name, "severity": result.severity, "date": result.date.strftime("%Y-%m-%d")} for
        result in results]

    return symptoms_data


@app.get("/filtered_symptoms/")
def get_filtered_symptoms(start_date: str, end_date: str, db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Symptom.symptom_name,
            func.avg(models.Symptom.severity).label("average_severity"),
            models.CheckIn.date
        )
        .join(models.CheckIn)
        .filter(models.CheckIn.date >= start_date, models.CheckIn.date <= end_date)
        .group_by(models.Symptom.symptom_name, models.CheckIn.date)
        .order_by(models.CheckIn.date)
        .all()
    )

    filtered_data = [
        {
            "symptom": result.symptom_name,
            "average_severity": result.average_severity,
            "date": result.date.strftime("%Y-%m-%d")
        }
        for result in results
    ]

    return filtered_data
