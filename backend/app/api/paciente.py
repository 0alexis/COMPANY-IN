from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.models import Paciente, Doctor
from ..schemas.paciente import PatientCreate, PatientResponse
from ..services.asignar_doctor import assign_doctor_to_patient  
from ..services.auth import get_medico_actual  




router = APIRouter(prefix="/pacientes", tags=["Pacientes"])

# Crear un paciente con doctor asignado
@router.post("/", response_model=PatientResponse)

def create_paciente(paciente: PatientCreate, db: Session = Depends(get_db)):
 # Si paciente.doctor_id es None, NO validamos nada
    if paciente.doctor_id is not None:
        doctor = db.query(Doctor).filter(Doctor.id == paciente.doctor_id).first()
        if not doctor:
            raise HTTPException(status_code=400, detail=f"No existe un doctor con el ID {paciente.doctor_id}")

    # Guardamos el paciente en la base de datos
    db_paciente = Paciente(
        name=paciente.name,
        cedula=paciente.cedula,
        doctor_id=paciente.doctor_id  # Puede ser None
    )
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

# Endpoint para asignar manualmente un doctor a un paciente sin doctor
from pydantic import BaseModel

class AssignDoctorRequest(BaseModel):
    doctor_id: int

@router.post("/{paciente_id}/asignar", response_model=PatientResponse)
def assign_doctor_manual(
    paciente_id: int,
    assignment: AssignDoctorRequest,
    db: Session = Depends(get_db),
    doctor: Doctor = Depends(get_medico_actual)  

):
    # Verificar que el paciente exista
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Verificar que el doctor exista
    doctor = db.query(Doctor).filter(Doctor.id == assignment.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    
    # Asignar el doctor manualmente
    paciente.doctor_id = doctor.id
    # Opcional: Actualizar la fecha de asignación, por ejemplo:
    # paciente.ultima_consulta = datetime.utcnow()

    try:
        db.commit()
        db.refresh(paciente)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al asignar el doctor") from e

    return paciente

##################################################    


#actualizar un paciente por id con doctor
@router.put("/{id}", response_model=PatientResponse)
def update_patient(id: int, paciente: PatientCreate, 
db: Session = Depends(get_db),
 doctor: Doctor = Depends(get_medico_actual)):

    # Verifica si el paciente existe
    db_paciente = db.query(Paciente).filter(Paciente.id == id).first()
    if not db_paciente:

        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    # Verifica si el doctor existe
    doctor = db.query(Doctor).filter(Doctor.id == paciente.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")

   # Verifica si el paciente ya está asignado a otro médico
    existing_paciente = db.query(Paciente).filter(Paciente.cedula == paciente.cedula, Paciente.id != id).first()
    if existing_paciente:
        raise HTTPException(status_code=400, detail="El paciente ya está asignado a otro médico")

   # Actualiza los cambios
    for key, value in paciente.dict().items():
        setattr(db_paciente, key, value)

    db.commit()
    db.refresh(db_paciente)
    return db_paciente

#obtener todos los pacientes
@router.get("/", response_model=list[PatientResponse])
def get_all_patients(db: Session = Depends(get_db)):
    # Obtener todos los pacientes con su doctor
    pacientes = db.query(Paciente).options(joinedload(Paciente.doctor)).all()
    return pacientes    

#obtener un paciente por ID
@router.get("/{id}", response_model=PatientResponse)
def get_patient(id: int, db: Session = Depends(get_db)):
    # Obtener el paciente con su doctor
    paciente = (
        db.query(Paciente)
        .options(joinedload(Paciente.doctor))
        .filter(Paciente.id == id)
        .first()
    )
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

# Eliminar un paciente por ID
@router.delete("/{id}", status_code=204)
def delete_patient(id: int, db: Session = Depends(get_db),
 doctor: Doctor = Depends(get_medico_actual)):

    paciente = db.query(Paciente).filter(Paciente.id == id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    db.delete(paciente)
    db.commit()
    return None    



