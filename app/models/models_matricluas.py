from database.banco import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Matricula(Base):
    __tablename__ = 'matricula'

    matricula = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey('alunos.id'))
    curso_id = Column(Integer, ForeignKey('cursos.id'))
