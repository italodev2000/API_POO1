from flask import Blueprint, jsonify, request
# Importa o serviço refatorado
from app.services.regras_service import AlunoService
# Importa a sessão do banco de dados
from database.banco import SessionLocal

# Inicialização do Blueprint e do Serviço
router = Blueprint("rotas", __name__)
service = AlunoService()


@router.route("/", methods=["GET"])
def home():
    """Rota de teste simples."""
    return {"Api": "Rodando perfeitamente!"}


def get_db():
    """Função para gerenciar a sessão do banco de dados (Injeção de Dependência)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        # Garante que a sessão seja fechada após o uso
        db.close()


@router.route("/alunos", methods=["GET"])
def listar_alunos():
    """Rota para listar todos os alunos."""
    db = next(get_db())

    # A rota apenas chama o serviço. O serviço retorna a lista já serializada.
    alunos_serializados = service.listar(db)

    # A rota apenas converte o resultado do serviço para JSON.
    return jsonify(alunos_serializados)


@router.route("/alunos", methods=["POST"])
def criar_aluno():
    """Rota para criar um novo aluno."""
    data = request.json
    db = next(get_db())

    # A rota apenas chama o serviço. O serviço retorna o aluno já serializado.
    aluno_serializado = service.criar(db, data["nome"], data["email"])

    # A rota apenas converte o resultado do serviço para JSON e define o status.
    return jsonify(aluno_serializado), 201


@router.route("/alunos/buscar", methods=["GET"])
def buscar_aluno_por_nome():
    """Rota para buscar alunos por nome (exemplo de uso do novo método)."""
    # Pega o nome do aluno dos parâmetros da query string (ex: /alunos/buscar?nome=Joao)
    nome_aluno = request.args.get("nome")

    if not nome_aluno:
        return jsonify({"erro": "Parâmetro 'nome' é obrigatório"}), 400

    db = next(get_db())

    # A rota apenas chama o serviço. O serviço retorna a lista já serializada.
    alunos_serializados = service.buscar_aluno(db, nome_aluno)

    # A rota apenas converte o resultado do serviço para JSON.
    return jsonify(alunos_serializados)
