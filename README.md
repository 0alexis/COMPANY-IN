# Proyecto Backend - API de Gestión de Médicos

Este es el backend para la aplicación de gestión de médicos, construida con **FastAPI**. Este proyecto maneja el registro, autenticación y gestión de médicos en una base de datos. Además, permite la protección de ciertos endpoints utilizando tokens JWT para autenticación.

## Tecnologías Utilizadas
- **FastAPI**: Framework web para Python.
![FastAPI Logo](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)

- **SQLAlchemy**: ORM para interactuar con la base de datos.
- **JWT (JSON Web Token)**: Para la autenticación de usuarios.
- **Passlib**: Para la encriptación de contraseñas.
- **MySQL**: Base de datos para almacenar la información.

## Requisitos

Antes de ejecutar este proyecto, asegúrate de tener lo siguiente instalado:

- **Python 3.8+**: Puedes descargarlo desde [python.org](https://www.python.org/downloads/).
![Python Logo](https://www.python.org/static/community_logos/python-logo.png)

- **pip**: El gestor de paquetes de Python.
- **MySQL** (o cualquier otra base de datos compatible como PostgreSQL).
- **Git**: Para clonar el repositorio.

## Instalación

### 1. Clonar el repositorio

Primero, clona el repositorio desde GitHub en tu máquina local:

```bash
git clone https://github.com/0alexis/COMPANY-IN.git
cd tu_repositorio_backend
```

### 2. Crear un entorno virtual

Es recomendable crear un entorno virtual para el proyecto para aislar las dependencias:

```bash
Windows:

python -m venv venv
.\venv\Scripts\activate
```

```bash
Linux/macOS:

python3 -m venv venv
source venv/bin/activate
```

### 3.  Instalar las dependencias
Con el entorno virtual activado, instala las dependencias del proyecto:

```bash
pip install -r requirements.txt

```


### 4. Configurar la base de datos

Asegúrate de tener una base de datos MySQL o cualquier base de datos compatible configurada correctamente. 

### 5. Ejecutar el servidor de desarrollo
Una vez configurado todo, puedes iniciar el servidor de desarrollo de FastAPI utilizando Uvicorn:

```bash
uvicorn app.main:app --reload
```


MIT License

Copyright (c) 2025 Alexis Guaza

Se otorga permiso, de forma gratuita, a cualquier persona que obtenga una copia del software y los archivos de documentación asociados, para usar el Software sin restricciones, incluyendo, sin limitación, los derechos a usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y/o vender copias del Software, y a permitir a las personas a quienes se les proporcione el Software hacerlo, bajo las siguientes condiciones:

El aviso de copyright y este aviso de permiso deben incluirse en todas las copias o partes sustanciales del Software.




