from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# User Schema
class UserBase(BaseModel):
    age: int
    sex: str
    country: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    user_id: int
    checkins: List["Checkin"] = []

    class Config:
        orm_mode = True


# Checkin Schema
class CheckinBase(BaseModel):
    date: date


class CheckinCreate(CheckinBase):
    user_id: int


class Checkin(CheckinBase):
    checkin_id: int
    symptoms: List["Symptom"] = []
    treatments: List["Treatment"] = []
    tags: List["Tag"] = []
    weather: Optional["Weather"] = None

    class Config:
        orm_mode = True


# Symptom Schema
class SymptomBase(BaseModel):
    symptom_name: str
    severity: int


class SymptomCreate(SymptomBase):
    checkin_id: int


class Symptom(SymptomBase):
    symptom_id: int

    class Config:
        orm_mode = True


# Treatment Schema
class TreatmentBase(BaseModel):
    treatment_name: str


class TreatmentCreate(TreatmentBase):
    checkin_id: int


class Treatment(TreatmentBase):
    treatment_id: int

    class Config:
        orm_mode = True


# Tag Schema
class TagBase(BaseModel):
    tag_name: str


class TagCreate(TagBase):
    checkin_id: int


class Tag(TagBase):
    tag_id: int

    class Config:
        orm_mode = True


# Weather Schema
class WeatherBase(BaseModel):
    description: Optional[str]
    temperature: Optional[float]
    humidity: Optional[float]
    pressure: Optional[float]


class WeatherCreate(WeatherBase):
    checkin_id: int


class Weather(WeatherBase):
    weather_id: int

    class Config:
        orm_mode = True
