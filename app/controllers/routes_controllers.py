from flask import Blueprint, jsonify, request
from app.services.regras_service import AlunoService, CursoService, MatriculaService
from database.banco import SessionLocal

router = Blueprint("rotas", __name__)
aluno_service = AlunoService()
curso_service = CursoService()
matricula_service = MatriculaService()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.route("/", methods=["GET"])
def home():
    return {"api": "Rodando perfeitamente!"}


@router.route("/alunos", methods=["GET"])
def listar_alunos():
    db = next(get_db())
    alunos = aluno_service.listar(db)
    return jsonify(alunos)


@router.route("/alunos", methods=["POST"])
def criar_aluno():
    data = request.get_json()
    db = next(get_db())
    aluno = aluno_service.criar(
        db,
        data.get("nome"),
        data.get("email"),
    )
    return jsonify(aluno)


@router.route("/cursos", methods=["GET"])
def listar_cursos():
    db = next(get_db())
    cursos = curso_service.listar_cursos(db)
    return jsonify(cursos)


@router.route("/cursos", methods=["POST"])
def criar_curso():
    data = request.get_json()
    db = next(get_db())
    curso = curso_service.criar_curso(
        db,
        data.get("nome"),
        data.get("descricao")
    )
    return jsonify(curso)


@router.route("/matriculas", methods=["GET"])
def listar_matriculas():
    db = next(get_db())
    matriculas = matricula_service.listar_matriculas(db)
    return jsonify(matriculas)
