import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    
    print("WARNING: DATABASE_URL no está configurada. Usando una URL dummy.")
    DATABASE_URL = "postgresql://dummy:dummy@localhost:5432/dummy"


try:
    engine = create_engine(DATABASE_URL)
    print("Conectado a la BD correctamente")
except SQLAlchemyError as e:
    print(f"Error al conectar a la BD: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Proporciona una sesión de base de datos a los endpoints de FastAPI y se asegura de cerrarla.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        
        db.close()