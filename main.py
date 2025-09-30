import os
import uvicorn
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db, Base, engine
from models import Estudiante
from schemas import Estudiante as EstudianteSchema, EstudianteCreate, EstudianteUpdate



# ----------------------------------------------------
# 1. Configuración de la Aplicación
# ----------------------------------------------------

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="API de Gestión de Estudiantes (PostgreSQL/Supabase)",
    description="API RESTful para realizar operaciones CRUD sobre la tabla 'estudiantes'.",
    version="1.0.0"
)


# ----------------------------------------------------
# 2. Endpoints (Rutas) de la API
# ----------------------------------------------------

@app.get(
    "/estudiantes/", 
    response_model=List[EstudianteSchema],
    summary="Listar todos los estudiantes",
    description="Devuelve una lista de todos los estudiantes registrados en la base de datos."
)
def listar_estudiantes(db: Session = Depends(get_db)):
    """
    GET /estudiantes/
    """
    estudiantes = db.query(Estudiante).all()
    return estudiantes

@app.get(
    "/estudiantes/{id}", 
    response_model=EstudianteSchema,
    summary="Obtener un estudiante por ID",
    description="Devuelve la información de un estudiante específico usando su ID."
)
def obtener_estudiante(id: int, db: Session = Depends(get_db)):
    """
    GET /estudiantes/{id}
    """
    # Consulta a la base de datos por ID
    estudiante = db.query(Estudiante).filter(Estudiante.id == id).first()
    
    # Manejo de error si no se encuentra el estudiante (HTTP 404)
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Estudiante con ID {id} no encontrado."
        )
    return estudiante

@app.post(
    "/estudiantes/", 
    response_model=EstudianteSchema, 
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo estudiante",
    description="Crea un nuevo registro de estudiante. Valida nombre, edad (>0), email (único) y foto_url (URL válida)."
)
def crear_estudiante(estudiante: EstudianteCreate, db: Session = Depends(get_db)):
    """
    POST /estudiantes/
    """
    # Crear una nueva instancia del modelo ORM a partir de los datos validados de Pydantic
    nuevo_estudiante = Estudiante(**estudiante.model_dump())
    
    try:
        # Añadir a la sesión y hacer commit
        db.add(nuevo_estudiante)
        db.commit()
        db.refresh(nuevo_estudiante) # Recargar el objeto para obtener el ID generado por la BD
        return nuevo_estudiante
    except IntegrityError:
        # Manejo de error de integridad (por ejemplo, si el email ya existe)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad: El email ya está registrado o datos inválidos."
        )

@app.put(
    "/estudiantes/{id}", 
    response_model=EstudianteSchema,
    summary="Actualizar un estudiante",
    description="Actualiza los datos de un estudiante existente usando su ID. Los campos son opcionales."
)
def actualizar_estudiante(id: int, estudiante_update: EstudianteUpdate, db: Session = Depends(get_db)):
    """
    PUT /estudiantes/{id}
    """
    estudiante = db.query(Estudiante).filter(Estudiante.id == id).first()
    
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Estudiante con ID {id} no encontrado."
        )

   
    update_data = estudiante_update.model_dump(exclude_unset=True)
    
   
    for key, value in update_data.items():
        setattr(estudiante, key, value)
        
    try:
        db.add(estudiante)
        db.commit()
        db.refresh(estudiante)
        return estudiante
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad: El email ya está registrado o datos inválidos."
        )

@app.delete(
    "/estudiantes/{id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un estudiante",
    description="Elimina un estudiante de la base de datos usando su ID."
)
def eliminar_estudiante(id: int, db: Session = Depends(get_db)):
    """
    DELETE /estudiantes/{id}
    """
    estudiante = db.query(Estudiante).filter(Estudiante.id == id).first()
    
    if not estudiante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Estudiante con ID {id} no encontrado."
        )
        
    # Eliminar y hacer commit
    db.delete(estudiante)
    db.commit()
    return {"ok": True} # Retorna 204 No Content por el status_code definido

# ----------------------------------------------------
# 3. Configuración de Ejecución (Uvicorn)
# ----------------------------------------------------

if __name__ == "__main__":
    
    port = int(os.getenv("PORT", 8000)) 
    
    
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=port, 
        reload=True 
    )
