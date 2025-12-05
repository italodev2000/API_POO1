from main import app, db_session
from flask import jsonify, request
from ..services.regras_service import AlunoService

aluno_service = AlunoService(db_session)


@app.route('/criar', methods=['POST'])
def criar_aluno():
    dados = request.json

    nome = dados.get("nome_aluno")
    cpf = dados.get("cpf")
    data_nascimento = dados.get("data_nascimento")
    telefone = dados.get("telefone_responsavel")
    email = dados.get("email")

    novo_aluno = aluno_service.criar_novo_aluno(
        nome_aluno=nome,
        cpf=cpf,
        data_nascimento=data_nascimento,
        telefone_responsavel=telefone,
        email=email
    )

    if novo_aluno:
        return jsonify({"mensagem": "Aluno criado com sucesso!"}), 201

    return jsonify({"erro": "Erro ao criar aluno"}), 400
