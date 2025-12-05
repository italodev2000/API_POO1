from database.banco import sessionlocal
from models.models_alunos import Aluno
from models.models_cursos import Curso
from models.models_matricluas import Matricula


class AlunoService:

    def __init__(self, db_session):
        self.db = db_session

    def criar_novo_aluno(self, nome_aluno, cpf, data_nascimento, telefone_responsavel, email):

        novo_aluno = Aluno(
            nome_aluno=nome_aluno,
            cpf=cpf,
            data_nascimento=data_nascimento,
            telefone_responsavel=telefone_responsavel,
            email=email
        )
        try:
            self.db.add(novo_aluno)
            self.db.commit()
            return novo_aluno
        except Exception as e:
            self.db.rollback()
            print(f"Erro ao criar aluno: {e}")
            return None
        finally:
            pass

    def buscar_aluno_por_nome_aluno(self, nome_aluno: str):

        try:
            aluno = (
                self.db.query(Aluno)
                .filter(Aluno.nome_aluno == nome_aluno).first())
            return aluno
        except Exception as e:
            print(f"Erro ao buscar aluno por CPF: {e}")
            return None
