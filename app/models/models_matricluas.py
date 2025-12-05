from sqlalchemy import Column, Integer, String, ForeignKey
from database.banco import base_dados


class Matricula(base_dados):
    __tablename__ = 'matricula'

    matricula = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey('alunos.id'))
    curso_id = Column(Integer, ForeignKey('cursos.id'))
