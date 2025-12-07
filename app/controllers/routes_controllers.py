# Conteúdo para app/controllers/routes_controllers.py (Com Novas Rotas)

from flask import Blueprint, jsonify, request
# Importa todos os serviços
from app.services.regras_service import AlunoService, CursoService, MatriculaService
# Importa a sessão do banco de dados
from database.banco import SessionLocal
# Importa os modelos (assumindo que estão em um local acessível)
# Para esta demonstração, usaremos os placeholders para referência
from app.models.models_alunos import Aluno
from app.models.models_cursos import Curso
from app.models.models_matricluas import Matricula

# Inicialização do Blueprint e dos Serviços
router = Blueprint("rotas", __name__)
aluno_service = AlunoService()
curso_service = CursoService()
matricula_service = MatriculaService()


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

# --- ROTAS DE ALUNO (EXISTENTES E NOVA) ---


@router.route("/alunos", methods=["GET"])
def listar_alunos():
    """Rota para listar todos os alunos."""
    db = next(get_db())
    # Passa o modelo Aluno para o serviço
    alunos_serializados = aluno_service.listar(db, Aluno)
    return jsonify(alunos_serializados)


@router.route("/alunos", methods=["POST"])
def criar_aluno():
    """Rota para criar um novo aluno."""
    data = request.json
    db = next(get_db())
    # Passa o modelo Aluno para o serviço
    aluno_serializado = aluno_service.criar(
        db, Aluno, data["nome"], data["email"])
    return jsonify(aluno_serializado), 201


@router.route("/alunos/buscar", methods=["GET"])
def buscar_aluno_por_nome():
    """Rota para buscar alunos por nome."""
    nome_aluno = request.args.get("nome")
    if not nome_aluno:
        return jsonify({"erro": "Parâmetro 'nome' é obrigatório"}), 400

    db = next(get_db())
    # Passa o modelo Aluno para o serviço
    alunos_serializados = aluno_service.buscar_aluno(db, Aluno, nome_aluno)
    return jsonify(alunos_serializados)


@router.route("/alunos/<int:aluno_id>", methods=["DELETE"])
def deletar_aluno(aluno_id):
    """NOVA ROTA: Deleta um aluno pelo ID."""
    db = next(get_db())
    # A rota apenas chama o serviço.
    deletado = aluno_service.deletar(db, Aluno, aluno_id)

    if deletado:
        # Retorna 204 No Content para deleção bem-sucedida
        return "", 204
    else:
        return jsonify({"erro": f"Aluno com ID {aluno_id} não encontrado."}), 404

# --- ROTAS DE CURSO (NOVAS) ---


@router.route("/cursos", methods=["GET"])
def listar_cursos():
    """NOVA ROTA: Lista todos os cursos."""
    db = next(get_db())
    # A rota apenas chama o serviço.
    cursos_serializados = curso_service.listar_cursos(db, Curso)
    return jsonify(cursos_serializados)


@router.route("/cursos/buscar", methods=["GET"])
def buscar_cursos():
    """NOVA ROTA: Busca cursos por nome ou matrícula (código)."""
    nome = request.args.get("nome")
    codigo = request.args.get("codigo")  # Usado como "matrícula" do curso

    if not nome and not codigo:
        return jsonify({"erro": "Pelo menos um parâmetro ('nome' ou 'codigo') é obrigatório."}), 400

    db = next(get_db())
    # A rota apenas chama o serviço.
    cursos_serializados = curso_service.buscar_curso(
        db, Curso, nome=nome, codigo=codigo)
    return jsonify(cursos_serializados)

# --- ROTAS DE MATRÍCULA (NOVA) ---


@router.route("/matriculas/<int:matricula_id>", methods=["GET"])
def buscar_matricula_por_id(matricula_id):
    """NOVA ROTA: Busca uma matrícula pelo ID."""
    db = next(get_db())
    # A rota apenas chama o serviço.
    matricula_serializada = matricula_service.buscar_matricula_por_id(
        db, Matricula, matricula_id)

    if matricula_serializada:
        return jsonify(matricula_serializada)
    else:
        return jsonify({"erro": f"Matrícula com ID {matricula_id} não encontrada."}), 404
