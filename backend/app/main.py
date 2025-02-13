from fastapi import FastAPI
from .db.database import Base, engine
from .api import doctor
from .api import paciente
from .api import auth

# Crear las tablas en MySQL si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Doctores y Pacientes")

app.include_router(auth.router)
app.include_router(doctor.router)
app.include_router(paciente.router)

@app.get("/")
def root():
    return {"message": "API en ejecución correctamente"}
