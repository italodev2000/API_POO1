# Conteúdo para app/services/servicos_refatorados.py (Substitui regras_service.py)

# IMPORTANTE: Você deve garantir que as classes Aluno, Curso e Matricula
# sejam importadas corretamente de seus respectivos arquivos de modelos (ex: app.models.models_alunos, etc.)
# Para esta demonstração, assumimos que elas estão disponíveis.
from app.models.models_alunos import Aluno
from app.models.models_cursos import Curso
from app.models.models_matricluas import Matricula

from sqlalchemy.exc import IntegrityError as DBIntegrityError
from sqlalchemy.exc import SQLAlchemyError as DBError
from datetime import datetime


def _serializar_entidade(entidade) -> dict:
    """Serializa a entidade para dicionário."""
    if not entidade:
        return None
    return {
        "id": entidade.id,
        "nome": getattr(entidade, 'nome', None),
        "apresentacao": entidade.apresentar(),
    }

# --- CLASSE DE SERVIÇO SIMPLIFICADA ---


class AlunoService:

    def listar(self, db):
        """Lista todos os alunos com try/except para leitura."""
        try:
            alunos = db.query(Aluno).all()
            return [_serializar_entidade(a) for a in alunos]
        except DBError as e:
            print(f"Erro ao listar alunos: {e}")
            # Retorna uma lista vazia em caso de erro de leitura
            return []
        except Exception as e:
            print(f"Erro inesperado ao listar: {e}")
            return []

    def criar(self, db, nome, email, matricula):
        """Cria um novo aluno com try/except para escrita."""
        try:
            aluno = Aluno(nome=nome, email=email, matricula=matricula)
            db.add(aluno)
            db.commit()
            db.refresh(aluno)
            return _serializar_entidade(aluno)
        except DBIntegrityError:
            db.rollback()
            # Retorna um erro específico para a rota
            return {"erro": "Aluno com esta matrícula ou e-mail já existe."}, 409
        except DBError as e:
            db.rollback()
            print(f"Erro ao criar aluno: {e}")
            # Retorna um erro genérico para a rota
            return {"erro": "Erro interno ao salvar aluno."}, 500
        except Exception as e:
            db.rollback()
            print(f"Erro inesperado: {e}")
            return {"erro": "Erro inesperado no serviço."}, 500

# --- Classe MatriculaService (Exemplo de Decisão com Try/Except) ---


class CursoService:

    def listar_cursos(self, db):
        """Repetição: Lista todos os cursos com tratamento de exceção."""
        try:
            cursos = db.query(Curso).all()
            return [_serializar_entidade(c) for c in cursos]
        except DBError as e:
            print(f"Erro ao listar cursos: {e}")
            return []


class MatriculaService:

    def _verificar_matricula_existente(self, db, aluno_id, curso_id):
        """Verifica se o aluno já está matriculado no curso."""
        try:
            matricula = db.query(Matricula).filter(
                Matricula.aluno_id == aluno_id,
                Matricula.curso_id == curso_id
            ).first()
            return bool(matricula)
        except DBError as e:
            print(f"Erro ao verificar matrícula: {e}")
            # Em caso de erro de leitura, assume True para evitar duplicidade
            return True

    def matricular_aluno(self, db, aluno_id, curso_id):
        """Matricula um aluno em um curso com verificação e try/except."""

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
