import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decimal import Decimal
import json

# Clase para serializar objetos Decimal en JSON
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # Convertir Decimal a float para JSON
        return super(DecimalEncoder, self).default(obj)

# Cargar variables de entorno
load_dotenv()

# Configuración de la conexión a la base de datos
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# URL de conexión a la base de datos
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Configurar la serialización JSON para manejar objetos Decimal
json_serializer = lambda obj: json.dumps(obj, cls=DecimalEncoder)

# Crear el engine de SQLAlchemy con serializador JSON personalizado
engine = create_engine(DATABASE_URL, json_serializer=json_serializer)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para los modelos
Base = declarative_base()

# Metadata para gestión de esquemas
metadata = MetaData()

def get_db():
    """
    Función para obtener una sesión de la base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
