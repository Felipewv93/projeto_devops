from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from pydantic import BaseModel
from typing import List
import pandas as pd

# Configuração do banco de dados
DATABASE_URL = os.environ.get("DATABASE_URL")  # ex: postgresql://user:pass@host:port/db
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo SQLAlchemy
class FilmeDB(Base):
    __tablename__ = "filmes"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    diretor = Column(String(50), nullable=False)
    estudio = Column(String(100), nullable=False)  # múltiplos estúdios separados por "/"
    genero = Column(String(50), nullable=False)
    ano = Column(Integer, nullable=False)
    bilheteria = Column(BigInteger, nullable=False)

# Modelo Pydantic para leitura
class Filme(BaseModel):
    id: int
    titulo: str
    diretor: str
    estudio: str
    genero: str
    ano: int
    bilheteria: int

    class Config:
        orm_mode = True

# Modelo Pydantic para criação
class FilmeCreate(BaseModel):
    titulo: str
    diretor: str
    estudio: str
    genero: str
    ano: int
    bilheteria: int

# Dependência para sessão do DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="API de Filmes")

# Endpoints

# Listar todos os filmes
@app.get("/filmes", response_model=List[Filme])
def listar_filmes(db: Session = Depends(get_db)):
    return db.query(FilmeDB).all()

# Criar novo filme
@app.post("/filmes", response_model=Filme)
def criar_filme(filme: FilmeCreate, db: Session = Depends(get_db)):
    novo_filme = FilmeDB(**filme.dict())
    db.add(novo_filme)
    db.commit()
    db.refresh(novo_filme)
    return novo_filme

# Análise por gênero
@app.get("/filmes/analise")
def analise_genero(db: Session = Depends(get_db)):
    filmes = db.query(FilmeDB).all()
    df = pd.DataFrame([{
        "titulo": f.titulo,
        "genero": f.genero,
        "bilheteria": f.bilheteria
    } for f in filmes])
    resumo = df.groupby("genero").agg(
        total_filmes=pd.NamedAgg(column="titulo", aggfunc="count"),
        bilheteria_total=pd.NamedAgg(column="bilheteria", aggfunc="sum"),
        bilheteria_media=pd.NamedAgg(column="bilheteria", aggfunc="mean")
    ).reset_index()
    return resumo.to_dict(orient="records")

# Análise por estúdio
@app.get("/filmes/analise_estudios")
def analise_estudios(db: Session = Depends(get_db)):
    filmes = db.query(FilmeDB).all()
    df = pd.DataFrame([{
        "titulo": f.titulo,
        "bilheteria": f.bilheteria,
        "estudios": f.estudio
    } for f in filmes])
    df = df.assign(estudio=df["estudios"].str.split("/")).explode("estudio")
    df["estudio"] = df["estudio"].str.strip()
    resumo = df.groupby("estudio").agg(
        total_filmes=pd.NamedAgg(column="titulo", aggfunc="count"),
        bilheteria_total=pd.NamedAgg(column="bilheteria", aggfunc="sum"),
        bilheteria_media=pd.NamedAgg(column="bilheteria", aggfunc="mean")
    ).reset_index()
    return resumo.to_dict(orient="records")
