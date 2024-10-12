from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    user_id: str
    age: Optional[int] = None
    sex: Optional[str] = None
    country: Optional[str] = None


class Checkin(BaseModel):
    checkin_id: int
    user_id: str
    date: str


class Symptom(BaseModel):
    symptom_id: int
    checkin_id: int
    symptom_name: str
    severity: int


class Treatment(BaseModel):
    treatment_id: int
    checkin_id: int
    treatment_name: str


class Tag(BaseModel):
    tag_id: int
    checkin_id: int
    tag_name: str


class Weather(BaseModel):
    weather_id: int
    checkin_id: int
    description: str
    temperature: Optional[float] = None
    humidity: float
    pressure: float


class UserCreate(BaseModel):
    age: int
    sex: str
    country: str


class CheckinCreate(BaseModel):
    user_id: int
    date: str


class SymptomCreate(BaseModel):
    checkin_id: int
    symptom_name: str
    severity: int


class TreatmentCreate(BaseModel):
    checkin_id: int
    treatment_name: str


class TagCreate(BaseModel):
    checkin_id: int
    tag_name: str


class WeatherCreate(BaseModel):
    checkin_id: int
    description: str
    temperature: float
    humidity: float
    pressure: float
