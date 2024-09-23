from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=True)
    sex = Column(String, nullable=True)
    country = Column(String, nullable=True)

    check_ins = relationship("CheckIn", back_populates="user")


class CheckIn(Base):
    __tablename__ = "checkins"

    checkin_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    date = Column(Date, nullable=False)

    user = relationship("User", back_populates="check_ins")
    symptoms = relationship("Symptom", back_populates="checkin")
    treatments = relationship("Treatment", back_populates="checkin")
    tags = relationship("Tag", back_populates="checkin")
    weather_records = relationship("Weather", back_populates="checkin")


class Symptom(Base):
    __tablename__ = "symptoms"

    symptom_id = Column(Integer, primary_key=True, index=True)
    checkin_id = Column(Integer, ForeignKey("checkins.checkin_id"))
    symptom_name = Column(String, nullable=False)
    severity = Column(Integer, nullable=False)

    checkin = relationship("CheckIn", back_populates="symptoms")


class Treatment(Base):
    __tablename__ = "treatments"

    treatment_id = Column(Integer, primary_key=True, index=True)
    checkin_id = Column(Integer, ForeignKey("checkins.checkin_id"))
    treatment_name = Column(String, nullable=False)

    checkin = relationship("CheckIn", back_populates="treatments")


class Tag(Base):
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True, index=True)
    checkin_id = Column(Integer, ForeignKey("checkins.checkin_id"))
    tag_name = Column(String, nullable=False)

    checkin = relationship("CheckIn", back_populates="tags")


class Weather(Base):
    __tablename__ = "weather"

    weather_id = Column(Integer, primary_key=True, index=True)
    checkin_id = Column(Integer, ForeignKey("checkins.checkin_id"))
    description = Column(String, nullable=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    pressure = Column(Float, nullable=True)

    checkin = relationship("CheckIn", back_populates="weather_records")
