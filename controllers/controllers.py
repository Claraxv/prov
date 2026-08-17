from flask import jsonify, request
from services.services import AlunoServices

class AlunoController():

    @staticmethod
    def valida_dados(dados):
        if not dados:
            return jsonify({"erro": "JSON inválido"}), 400
        if len(dados.get("nome", "")) < 3:
            return jsonify({"erro": "Nome inválido"}), 400
        idade = dados.get("idade")
        if idade is None:
            return jsonify({"erro": "Idade obrigatória"}), 400
        if idade < 5:
            return jsonify({"erro": "Idade mínima é 5 anos"}), 400
        if idade > 120:
            return jsonify({"erro": "Idade inválida"}), 400
        email = dados.get("email")
        if not email:
            return jsonify({"erro": "Email obrigatório"}), 400
        if "@" not in email:
            return jsonify({"erro": "Email inválido"}), 400
        curso = dados.get("curso")
        if not curso:
            return jsonify({"erro": "Curso obrigatório"}), 400
        return True
        
    @staticmethod
    def index():
        return "Hello World!"
        
    @staticmethod
    def listar():
        nome = request.args.get("nome")
        curso = request.args.get("curso")
        ativo = request.args.get("ativo")
        resultado = AlunoServices.consulta_alunos(nome=nome, curso=curso, ativo=ativo)
        return jsonify(resultado)

    @staticmethod
    def cadastrar():
        dados = request.json
        valida_dados = AlunoController.valida_dados(dados)
        if valida_dados is not True:
            return valida_dados

        aluno = AlunoServices.cadastra_aluno(
            nome=dados["nome"],
            idade=dados["idade"],
            email=dados["email"],
            curso=dados["curso"],
            ativo=dados.get("ativo", True)
        )

        return jsonify({
            "mensagem": "Aluno cadastrado",
            "id": aluno.id
        })

    @staticmethod
    def atualizar(id):
        dados = request.json
        valida_dados = AlunoController.valida_dados(dados)
        if valida_dados is not True:
            return valida_dados

        aluno = AlunoServices.atualiza_aluno(
            id=id,
            nome=dados["nome"],
            idade=dados["idade"],
            email=dados["email"],
            curso=dados["curso"]
        )

        if not aluno:
            return jsonify({"erro": "Aluno não encontrado"}), 404

        return jsonify({
            "mensagem": "Aluno atualizado",
            "id": aluno.id
        })

    @staticmethod
    def excluir(id):
        aluno = AlunoServices.exclui_aluno(id)
        if not aluno:
            return jsonify({"erro": "Aluno não encontrado"}), 404
        return jsonify({
            "mensagem": "Aluno excluído",
            "id": aluno.id
        })

    @staticmethod
    def ativar(id):
        aluno = AlunoServices.ativa_aluno(id)
        if not aluno:
            return jsonify({"erro": "Aluno não encontrado"}), 404
        return jsonify({
            "mensagem": "Aluno ativado",
            "id": aluno.id
        })

    @staticmethod
    def desativar(id):
        aluno = AlunoServices.desativa_aluno(id)
        if not aluno:
            return jsonify({"erro": "Aluno não encontrado"}), 404
        return jsonify({
            "mensagem": "Aluno desativado",
            "id": aluno.id
        })

    @staticmethod
    def estatisticas():
        estatisticas = AlunoServices.gera_estatisticas()
        return jsonify(estatisticas)