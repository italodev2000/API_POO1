
from flask import Blueprint, jsonify, request
from app.services.regras_service import AlunoService, CursoService, MatriculaService
from database.banco import SessionLocal
from app.models.models_alunos import Aluno
from app.models.models_cursos import Curso
from app.models.models_matricluas import Matricula


router = Blueprint("rotas", __name__)
aluno_service = AlunoService()
curso_service = CursoService()
matricula_service = MatriculaService()


@router.route("/", methods=["GET"])
def home():
    """Rota de teste simples."""
    return {"Api": "Rodando perfeitamente!"}


def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:

        db.close()


@router.route("/alunos", methods=["GET"])
def listar_alunos():

    db = next(get_db())

    alunos_serializados = aluno_service.listar(db, Aluno)
    return jsonify(alunos_serializados)


@router.route("/alunos", methods=["POST"])
def criar_aluno():

    data = request.json
    db = next(get_db())

    aluno_serializado = aluno_service.criar(
        db, Aluno, data["nome"], data["email"])
    return jsonify(aluno_serializado),


@router.route("/alunos/buscar", methods=["GET"])
def buscar_aluno_por_nome():

    nome_aluno = request.args.get("nome")
    if not nome_aluno:
        return jsonify({"erro": "Parâmetro 'nome' é obrigatório"}),

    db = next(get_db())

    alunos_serializados = aluno_service.buscar_aluno(db, Aluno, nome_aluno)
    return jsonify(alunos_serializados)


@router.route("/cursos", methods=["GET"])
def listar_cursos():

    db = next(get_db())

    cursos_serializados = curso_service.listar_cursos(db, Curso)
    return jsonify(cursos_serializados)


@router.route("/matriculas/<int:matricula_id>", methods=["GET"])
def buscar_matricula_por_id(matricula_id):

    db = next(get_db())

    matricula_serializada = matricula_service.buscar_matricula_por_id(
        db, Matricula, matricula_id)

    if matricula_serializada:
        return jsonify(matricula_serializada)
    else:
        return jsonify({"erro": f"Matrícula com ID {matricula_id} não encontrada."}), 404
