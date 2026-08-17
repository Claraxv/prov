from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///escola.db" 
app.config["SECRET_KEY"] = 'minhachavesupersecretaqueninguemvaidescobrir'

db = SQLAlchemy(app)

class Aluno(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    curso = db.Column(db.String(80), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.now)

with app.app_context():
    db.create_all()


@app.route("/")
def index():

    alunos = Aluno.query.order_by(Aluno.nome).all()

    resultado = []

    for aluno in alunos:
        resultado.append({
            "id": aluno.id,
            "nome": aluno.nome,
            "idade": aluno.idade,
            "email": aluno.email,
            "curso": aluno.curso,
            "ativo": aluno.ativo,
            "data_cadastro": aluno.data_cadastro.strftime("%d/%m/%Y %H:%M")
        })

    return jsonify(resultado)


@app.route("/alunos", methods=["GET"])
def listar():

    nome = request.args.get("nome")
    curso = request.args.get("curso")
    ativo = request.args.get("ativo")

    if nome:
        alunos = Aluno.query.filter(
            Aluno.nome.like(f"%{nome}%")
        ).all()

    elif curso:
        alunos = Aluno.query.filter_by(
            curso=curso
        ).all()

    elif ativo is not None:

        if ativo.lower() == "true":
            alunos = Aluno.query.filter_by(ativo=True).all()
        else:
            alunos = Aluno.query.filter_by(ativo=False).all()

    else:
        alunos = Aluno.query.all()

    lista = []

    for aluno in alunos:
        lista.append({
            "id": aluno.id,
            "nome": aluno.nome,
            "idade": aluno.idade,
            "email": aluno.email,
            "curso": aluno.curso,
            "ativo": aluno.ativo
        })

    return jsonify(lista)


@app.route("/alunos/<int:id>")
def buscar(id):

    aluno = Aluno.query.get(id)

    if aluno is None:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    return jsonify({
        "id": aluno.id,
        "nome": aluno.nome,
        "idade": aluno.idade,
        "email": aluno.email,
        "curso": aluno.curso,
        "ativo": aluno.ativo,
        "data_cadastro": aluno.data_cadastro.strftime("%d/%m/%Y %H:%M")
    })


@app.route("/alunos", methods=["POST"])
def cadastrar():

    dados = request.json

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

    existe = Aluno.query.filter_by(email=email).first()

    if existe:
        return jsonify({"erro": "Email já cadastrado"}), 400

    curso = dados.get("curso")

    if not curso:
        return jsonify({"erro": "Curso obrigatório"}), 400

    aluno = Aluno()

    aluno.nome = dados["nome"]
    aluno.idade = idade
    aluno.email = email
    aluno.curso = curso
    aluno.ativo = True

    db.session.add(aluno)
    db.session.commit()

    return jsonify({
        "mensagem": "Aluno cadastrado",
        "id": aluno.id
    })


@app.route("/alunos/<int:id>", methods=["PUT"])
def atualizar(id):

    aluno = Aluno.query.get(id)

    if aluno is None:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    dados = request.json

    if "nome" in dados:

        if len(dados["nome"]) < 3:
            return jsonify({"erro": "Nome inválido"}), 400

        aluno.nome = dados["nome"]

    if "idade" in dados:

        if dados["idade"] < 5:
            return jsonify({"erro": "Idade inválida"}), 400

        aluno.idade = dados["idade"]

    if "email" in dados:

        outro = Aluno.query.filter_by(
            email=dados["email"]
        ).first()

        if outro and outro.id != aluno.id:
            return jsonify({"erro": "Email já utilizado"}), 400

        aluno.email = dados["email"]

    if "curso" in dados:
        aluno.curso = dados["curso"]

    if "ativo" in dados:
        aluno.ativo = dados["ativo"]

    db.session.commit()

    return jsonify({
        "mensagem": "Aluno atualizado"
    })


@app.route("/alunos/<int:id>", methods=["DELETE"])
def excluir(id):

    aluno = Aluno.query.get(id)

    if aluno is None:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    db.session.delete(aluno)
    db.session.commit()

    return jsonify({
        "mensagem": "Aluno removido"
    })


@app.route("/alunos/<int:id>/ativar", methods=["PATCH"])
def ativar(id):

    aluno = Aluno.query.get(id)

    if aluno is None:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    aluno.ativo = True

    db.session.commit()

    return jsonify({
        "mensagem": "Aluno ativado"
    })


@app.route("/alunos/<int:id>/desativar", methods=["PATCH"])
def desativar(id):

    aluno = Aluno.query.get(id)

    if aluno is None:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    aluno.ativo = False

    db.session.commit()

    return jsonify({
        "mensagem": "Aluno desativado"
    })


@app.route("/estatisticas")
def estatisticas():

    total = Aluno.query.count()

    ativos = Aluno.query.filter_by(
        ativo=True
    ).count()

    inativos = Aluno.query.filter_by(
        ativo=False
    ).count()

    cursos = db.session.query(
        Aluno.curso
    ).distinct().count()

    return jsonify({
        "total_alunos": total,
        "ativos": ativos,
        "inativos": inativos,
        "cursos": cursos
    })

if __name__ == "__main__":
    app.run(debug=True)