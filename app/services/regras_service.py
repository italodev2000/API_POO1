
from app.models.models_alunos import Aluno
from app.models.models_cursos import Curso
from app.models.models_matricluas import Matricula

from sqlalchemy.exc import IntegrityError as DBIntegrityError
from sqlalchemy.exc import SQLAlchemyError as DBError
from datetime import datetime


def _serializar_entidade(entidade) -> dict:

    if not entidade:
        return None
    return {
        "id": entidade.id,
        "nome": getattr(entidade, 'nome', None),
        "apresentacao": entidade.apresentar(),
    }


class AlunoService:

    def listar(self, db):

        try:
            alunos = db.query(Aluno).all()
            return [_serializar_entidade(a) for a in alunos]
        except DBError as e:
            print(f"Erro ao listar alunos: {e}")

            return []
        except Exception as e:
            print(f"Erro inesperado ao listar: {e}")
            return []

    def criar(self, db, nome, email, matricula):

        try:
            aluno = Aluno(nome=nome, email=email, matricula=matricula)
            db.add(aluno)
            db.commit()
            db.refresh(aluno)
            return _serializar_entidade(aluno)
        except DBIntegrityError:
            db.rollback()

            return {"erro": "Aluno com esta matrícula ou e-mail já existe."},
        except DBError as e:
            db.rollback()
            print(f"Erro ao criar aluno: {e}")

            return {"erro": "Erro interno ao salvar aluno."},
        except Exception as e:
            db.rollback()
            print(f"Erro inesperado: {e}")
            return {"erro": "Erro inesperado no serviço."},


class CursoService:

    def listar_cursos(self, db):

        try:
            cursos = db.query(Curso).all()
            return [_serializar_entidade(c) for c in cursos]
        except DBError as e:
            print(f"Erro ao listar cursos: {e}")
            return []


class MatriculaService:

    def _verificar_matricula_existente(self, db, aluno_id, curso_id):

        try:
            matricula = db.query(Matricula).filter(
                Matricula.aluno_id == aluno_id,
                Matricula.curso_id == curso_id
            ).first()
            return bool(matricula)
        except DBError as e:
            print(f"Erro ao verificar matrícula: {e}")

            return True

    def matricular_aluno(self, db, aluno_id, curso_id):

        if self._verificar_matricula_existente(db, aluno_id, curso_id):
            return {"erro": "Aluno já está matriculado neste curso."}, 400

        try:
            matricula = Matricula(
                aluno_id=aluno_id, curso_id=curso_id, data_matricula=datetime.now())
            db.add(matricula)
            db.commit()
            db.refresh(matricula)
            return _serializar_entidade(matricula)
        except DBError as e:
            db.rollback()
            print(f"Erro ao matricular aluno: {e}")
            return {"erro": "Erro interno ao realizar matrícula."}, 500
