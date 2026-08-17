from repositories.repositories import AlunoRepository

class AlunoServices():
    @staticmethod
    def consulta_alunos(nome=None, curso=None, ativo=None):
        alunos = AlunoRepository.consulta_tudo(nome=nome, curso=curso, ativo=ativo)

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
        return resultado

    @staticmethod
    def cadastra_aluno(**kwargs):
        aluno = AlunoRepository.cadastrar_aluno(kwargs)
        return aluno

    @staticmethod
    def consultar_email(email):
        return AlunoRepository.pesquisa_email(email)

    @staticmethod
    def atualiza_aluno(id, **kwargs):
        aluno = AlunoRepository.atualizar_aluno(id, kwargs)
        return aluno

    @staticmethod
    def exclui_aluno(id):
        aluno = AlunoRepository.excluir_aluno(id)
        return aluno

    @staticmethod
    def ativa_aluno(id):
        aluno = AlunoRepository.ativar_aluno(id)
        return aluno

    @staticmethod
    def desativa_aluno(id):
        aluno = AlunoRepository.desativar_aluno(id)
        return aluno

    @staticmethod
    def gera_estatisticas():
        total = AlunoRepository.conta_total_alunos()
        ativos = AlunoRepository.conta_alunos_ativos()
        inativos = total - ativos
        cursos = AlunoRepository.conta_cursos()
        estatisticas = {
            "total_alunos": total,
            "ativos": ativos,
            "inativos": inativos,
            "cursos": cursos
        }
        return estatisticas