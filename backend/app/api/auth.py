from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..db.database import get_db
from ..db.models import Doctor
from ..schemas.doctor import DoctorCreate, DoctorResponse
from ..services.auth import get_password_hash
from ..services.auth import verify_password, create_access_token





router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=DoctorResponse)

def register_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    """Registra un nuevo médico con contraseña encriptada"""
    hashed_password = get_password_hash(doctor.password)  # Encripta la contraseña antes de guardarla

    db_doctor = Doctor(
        name=doctor.name,
        cedula=doctor.cedula,
        especialidad=doctor.especialidad,
        ciudad=doctor.ciudad,
        password = hashed_password  # Se guarda la contraseña encriptada
    )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@router.post("/login")
def login_doctor(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Autentica al médico y devuelve un token JWT"""
    doctor = db.query(Doctor).filter(Doctor.cedula == form_data.username).first()
    if not doctor or not verify_password(form_data.password, doctor.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    access_token = create_access_token(doctor_id=doctor.id)
    return {"access_token": access_token, "token_type": "bearer"}

   
