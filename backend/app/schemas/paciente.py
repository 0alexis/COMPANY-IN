from pydantic import BaseModel
from datetime import datetime
from typing import ForwardRef, Optional

DoctorResponse = ForwardRef('DoctorResponse')

class PatientBase(BaseModel):
    name: str
    cedula: str

class PatientCreate(PatientBase):
    doctor_id: Optional[int] = None    

class PatientResponse(PatientBase):
    id: int
    ultima_consulta: datetime
    
    doctor: Optional[DoctorResponse] = None  
   # doctor_id: Optional[int] = None 

    class Config:
        from_attributes = True

from .doctor import DoctorResponse
PatientResponse.update_forward_refs()     
