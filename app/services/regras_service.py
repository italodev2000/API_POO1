from app.models.models_alunos import Aluno
from app.models.models_cursos import Curso
from app.models.models_matricluas import Matricula

from sqlalchemy.exc import SQLAlchemyError


def serializar_aluno(aluno):
    return {
        "id": aluno.id,
        "nome": aluno.nome,
        "email": aluno.email
    }


def serializar_curso(curso):
    return {
        "id": curso.id,
        "nome_curso": curso.nome_curso,
        "carga_horaria": curso.carga_horaria,
        "periodo": curso.periodo,
        "mensalidade": curso.mensalidade
    }


def serializar_matricula(matricula):
    return {
        "id": matricula.id,
        "aluno": matricula.aluno.nome if matricula.aluno else None,
        "curso": matricula.curso.nome if matricula.curso else None,
        "data_matricula": matricula.data_matricula.strftime("%d/%m/%Y %H:%M:%S")
    }


class AlunoService:
    def listar(self, db):
        alunos = db.query(Aluno).all()
        return [serializar_aluno(a) for a in alunos]

    def criar(self, db, nome, email):
        novo_aluno = Aluno(nome=nome, email=email)
        db.add(novo_aluno)
        db.commit()
        db.refresh(novo_aluno)
        return serializar_aluno(novo_aluno)


class CursoService:
    def listar_cursos(self, db):
        cursos = db.query(Curso).all()
        return [serializar_curso(c) for c in cursos]

    def criar_curso(self, db, nome, descricao=None):
        novo_curso = Curso(nome=nome, descricao=descricao)
        db.add(novo_curso)
        db.commit()
        db.refresh(novo_curso)
        return serializar_curso(novo_curso)


class MatriculaService:
    def listar_matriculas(self, db):
        matriculas = db.query(Matricula).all()
        return [serializar_matricula(m) for m in matriculas]
