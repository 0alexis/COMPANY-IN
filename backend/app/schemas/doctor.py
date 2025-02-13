from pydantic import BaseModel
from typing import List, ForwardRef, Optional

PacienteResponse = ForwardRef('PatientResponse')


class DoctorBase(BaseModel):
    name: str
    cedula: str
    especialidad: str
    ciudad: str

class DoctorCreate(DoctorBase):
    pass
    password: str

class DoctorResponse(DoctorBase):
    id: int
    
    pacientes: List[PacienteResponse] = []  

    class Config:
        from_attributes = True

from .paciente import PatientResponse
DoctorResponse.update_forward_refs()