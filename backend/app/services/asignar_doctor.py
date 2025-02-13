from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from datetime import datetime
import logging
from ..db.models import Paciente, Doctor  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def assign_doctor_to_patient(db: Session, paciente: Paciente) -> bool:
    """
    Asigna un doctor a un paciente sin asignación.
    Selecciona el doctor con menor carga (número de pacientes) y asigna su ID.
    Retorna True si la asignación fue exitosa, False de lo contrario.
    """
    try:
        selected_doctor = (
            db.query(Doctor)
            .outerjoin(Doctor.patients)
            .group_by(Doctor.id)
            .order_by(func.count(Paciente.id))
            .first()
        )

        if not selected_doctor:
            logger.warning("No hay doctores disponibles para asignar")
            return False

        paciente.doctor_id = selected_doctor.id
        paciente.ultima_consulta = datetime.utcnow()

        db.commit()
        db.refresh(paciente)
        logger.info(f"Paciente {paciente.id} asignado al doctor {selected_doctor.id}")
        return True

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al asignar doctor a paciente: {e}")
        return False

def assign_doctors_for_unassigned_patients(db: Session):
    """
    Asigna doctores a todos los pacientes sin asignación.
    Retorna el número de pacientes asignados.
    """
    try:
        unassigned_patients = (
            db.query(Paciente)
            .filter(Paciente.doctor_id == None)
            .all()
        )

        if not unassigned_patients:
            logger.info("No hay pacientes sin asignación de doctor.")
            return

        for paciente in unassigned_patients:
            success = assign_doctor_to_patient(db, paciente)
            if not success:
                logger.warning(f"No se pudo asignar un doctor al paciente {paciente.id}.")

    except SQLAlchemyError as e:
        logger.error(f"Error en la asignación masiva de doctores: {e}")
