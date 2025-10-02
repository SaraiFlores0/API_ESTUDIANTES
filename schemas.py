from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional

# Clase base para la definición de un estudiante (campos comunes)
class EstudianteBase(BaseModel):
  
    nombre: str = Field(..., min_length=1, description="Nombre del estudiante. No puede ser vacío.")
    
    edad: int = Field(..., gt=0, description="Edad del estudiante. Debe ser mayor que 0.")
   
    correo: EmailStr = Field(..., description="Correo electrónico único del estudiante.")

    telefono: str = Field(..., min_length=7, max_length=15, description="Número de teléfono del estudiante.")
    
    foto_url: HttpUrl = Field(..., description="URL de la foto del estudiante (de Firebase, etc.).")
    

    class Config:
        from_attributes = True


class EstudianteCreate(EstudianteBase):
    pass


class EstudianteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, description="Nombre del estudiante (opcional).")
    edad: Optional[int] = Field(None, gt=0, description="Edad del estudiante (opcional). Debe ser mayor que 0.")
    correo: Optional[EmailStr] = Field(None, description="Correo electrónico (opcional). Debe ser único.")
    telefono: Optional[str] = Field(None, min_length=7, max_length=15, description="Número de teléfono (opcional).")
    foto_url: Optional[str] = Field(None, description="URL de la foto (opcional).")



class Estudiante(EstudianteBase):
    id: int = Field(..., description="ID autoincremental del estudiante.")
