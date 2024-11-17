from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sqlAlCHEMY_DATABASE_URL="postgresql://postgres:40284433@localhost/FastAPI"
engine=create_engine(sqlAlCHEMY_DATABASE_URL)
sessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()