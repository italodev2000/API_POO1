# Conteúdo para app/services/regras_service.py (Refatorado)

from app.models.models_alunos import Aluno
# Assumindo que a classe Aluno está definida e importada corretamente


class AlunoService:

    # Função auxiliar para serializar o objeto Aluno em um dicionário
    def _serializar_aluno(self, aluno: Aluno) -> dict:
        """Converte um objeto Aluno do ORM em um dicionário para resposta JSON."""
        return {
            "id": aluno.id,
            "nome": aluno.nome,
            "email": aluno.email
        }

    def listar(self, db):
        """Busca todos os alunos e retorna uma lista de dicionários."""
        alunos = db.query(Aluno).all()
        # A lógica de formatação (serialização) é movida para o serviço
        return [self._serializar_aluno(a) for a in alunos]

    def criar(self, db, nome, email):
        """Cria um novo aluno no banco de dados e retorna o aluno serializado."""
        aluno = Aluno(nome=nome, email=email)
        db.add(aluno)
        db.commit()
        db.refresh(aluno)
        # Retorna o aluno serializado
        return self._serializar_aluno(aluno)

    def buscar_aluno(self, db, nome_aluno):
        """Busca alunos por nome e retorna uma lista de dicionários."""
        # Correção: Adicionado .all() para executar a consulta
        alunos_encontrados = db.query(Aluno).filter(
            Aluno.nome == nome_aluno).all()
        # db.commit() removido por ser desnecessário em operações de leitura

        # Retorna a lista de alunos serializados
        return [self._serializar_aluno(a) for a in alunos_encontrados]
