from sqlalchemy import Column, Integer, String, Date
from database.banco import base_dados


class Aluno(base_dados):
    __tablename__ = 'alunos'

    id = Column(Integer, primary_key=True)
    nome_aluno = Column(String(200))
    cpf = Column(Integer)
    data_nascimento = Column(Date)
    telefone_responsavel = Column(Integer)
    email = Column(String(200))
