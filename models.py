from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Base declarativa para los modelos ORM
Base = declarative_base()

class Estudiante(Base):
    """
    Modelo ORM de SQLAlchemy para la tabla 'estudiantes'.
    Mapea las columnas de la base de datos PostgreSQL.
    """
    __tablename__ = 'estudiantes'
    
    # Columna 'id': Clave primaria, entero, autoincremental
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Columna 'nombre': Texto, requerido
    nombre = Column(String(200), nullable=False)
    
    # Columna 'edad': Entero, requerido
    edad = Column(Integer, nullable=False)
    
    # Columna 'email': Texto, requerido, único
    correo = Column(String(200), nullable=False)

    telefono = Column(String(50), nullable=False)
    
    # Columna 'foto_url': Texto (URL)
    foto_url = Column(Text, nullable=True) 
    
    def __repr__(self):
        return f"<Estudiante(id={self.id}, nombre='{self.nombre}', edad='{self.edad}, correo='{self.correo}', telefono='{self.telefono}', foto_url='{self.foto_url})>"
