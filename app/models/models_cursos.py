from database.banco import Base
from sqlalchemy import Column, Integer, String


class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True)
    nome_curso = Column(String(200))
    carga_horaria = Column(String(200))
    periodo = Column(String(200))
    mensalidade = Column(Integer)
