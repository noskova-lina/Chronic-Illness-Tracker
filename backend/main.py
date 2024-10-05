from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
import pandas as pd
from database import SessionLocal, engine
import models
import schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
                                                                   models.Symptom.symptom_name == row['trackable_name']).first()

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
