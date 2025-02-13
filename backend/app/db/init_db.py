from .database.datab import engine, Base

print("Creando tablas en MySQL...")
Base.metadata.create_all(bind=engine)
print("¡Tablas creadas correctamente en MySQL!")
