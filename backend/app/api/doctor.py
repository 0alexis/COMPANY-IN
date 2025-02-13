from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..db.models import Doctor
from ..schemas.doctor import DoctorCreate, DoctorResponse

router = APIRouter(prefix="/doctors", tags=["Doctors"])

# POST: Crear un nuevo doctor
@router.post("/", response_model=DoctorResponse)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

# GET: Obtener todos los doctores con pacientes asignados
@router.get("/", response_model=List[DoctorResponse])
def get_doctors(db: Session = Depends(get_db)):
    return db.query(Doctor).all()


# GET: Obtener un doctor por ID
@router.get("/{id}", response_model=DoctorResponse)
def get_doctor(id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    return doctor

# DELETE: Eliminar un doctor por ID
@router.delete("/{id}", status_code=204)
def delete_doctor(id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")

    db.delete(doctor)
    db.commit()
    return None