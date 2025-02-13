from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Doctor(Base):
    __tablename__ = "doctores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    cedula = Column(String(10), unique=True, index=True)
    especialidad = Column(String(30))
    ciudad = Column(String(20))
    password = Column(String(255)) 

    patients = relationship("Paciente", back_populates="doctor")

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    cedula = Column(String(10), unique=True, index=True)

    ultima_consulta = Column(DateTime, default=datetime.utcnow)

    doctor_id = Column(Integer, ForeignKey("doctores.id"), nullable=True)
    doctor = relationship("Doctor", back_populates="patients", lazy= "joined")
 
    