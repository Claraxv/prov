from models.models import Aluno
from database import db

class AlunoRepository():
    @staticmethod
    def consulta_tudo(nome=None, curso=None, ativo=None):
        if nome:
            return Aluno.query.filter(Aluno.nome.like(f"%{nome}%")).order_by(Aluno.nome).all()
        elif curso:
            return Aluno.query.filter_by(curso=curso).order_by(Aluno.nome).all()
        elif ativo is not None:
            if ativo.lower() == "true":
                return Aluno.query.filter_by(ativo=True).order_by(Aluno.nome).all()
            else:
                return Aluno.query.filter_by(ativo=False).order_by(Aluno.nome).all()
        return Aluno.query.order_by(Aluno.nome).all()

    @staticmethod
    def consulta_um(aluno_id):
        return Aluno.query.filter_by(id=aluno_id).first()

    @staticmethod
    def cadastrar_aluno(dados):
        aluno = Aluno(
            nome=dados['nome'],
            idade=dados['idade'],
            email=dados['email'],
            curso=dados['curso'],
            ativo=dados['ativo']
        )
        db.session.add(aluno)
        db.session.commit()
        return aluno

    @staticmethod
    def pesquisa_email(email):
        email = Aluno.query.filter_by(email=email).first()
        return email

    @staticmethod
    def atualizar_aluno(id, dados):
        aluno = Aluno.query.filter_by(id=id).first()
        if not aluno:
            return None
        aluno.nome = dados['nome']
        aluno.idade = dados['idade']
        aluno.email = dados['email']
        aluno.curso = dados['curso']
        db.session.commit()
        return aluno
    
    @staticmethod
    def excluir_aluno(id):
        aluno = Aluno.query.filter_by(id=id).first()
        if not aluno:
            return None
        db.session.delete(aluno)
        db.session.commit()
        return aluno

    @staticmethod
    def ativar_aluno(id):
        aluno = Aluno.query.filter_by(id=id).first()
        if not aluno:
            return None
        aluno.ativo = True
        db.session.commit()
        return aluno

    @staticmethod
    def desativar_aluno(id):
        aluno = Aluno.query.filter_by(id=id).first()
        if not aluno:
            return None
        aluno.ativo = False
        db.session.commit()
        return aluno

    @staticmethod
    def conta_total_alunos():
        return Aluno.query.count()

    @staticmethod
    def conta_alunos_ativos():
        return Aluno.query.filter_by(ativo=True).count()
    
    @staticmethod
    def conta_cursos():
        return db.session.query(Aluno.curso).distinct().count()