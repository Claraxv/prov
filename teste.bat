@echo off
chcp 65001 > nul
set BASE_URL=http://localhost:5000

echo ===================================================
echo INICIANDO TESTES NAS ROTAS DA APLICACAO FLASK
echo Target: %BASE_URL%
echo ===================================================
echo.

echo [1/9] GET / - (Página Inicial)
curl -X GET %BASE_URL%/
echo.
echo ---------------------------------------------------

echo [2/9] POST /alunos - (Cadastrar Aluno Válido)
curl -X POST %BASE_URL%/alunos ^
  -H "Content-Type: application/json" ^
  -d "{\"nome\": \"Carlos Silva\", \"idade\": 25, \"email\": \"carlos@email.com\", \"curso\": \"Engenharia\"}"
echo.
echo ---------------------------------------------------

echo [3/9] POST /alunos - (Cadastrar Aluno com Dados Inválidos - Espera-se Erro)
curl -X POST %BASE_URL%/alunos ^
  -H "Content-Type: application/json" ^
  -d "{\"nome\": \"An\", \"idade\": 3, \"email\": \"email_invalido\", \"curso\": \"\"}"
echo.
echo ---------------------------------------------------

echo [4/9] GET /alunos - (Listar Alunos)
curl -X GET %BASE_URL%/alunos
echo.
echo ---------------------------------------------------

echo [5/9] PUT /alunos/1 - (Atualizar Aluno ID 1)
curl -X PUT %BASE_URL%/alunos/1 ^
  -H "Content-Type: application/json" ^
  -d "{\"nome\": \"Carlos Silva Editado\", \"idade\": 26, \"email\": \"carlos.editado@email.com\", \"curso\": \"Ciencia da Computacao\"}"
echo.
echo ---------------------------------------------------

echo [6/9] PATCH /alunos/1/desativar - (Desativar Aluno ID 1)
curl -X PATCH %BASE_URL%/alunos/1/desativar
echo.
echo ---------------------------------------------------

echo [7/9] PATCH /alunos/1/ativar - (Ativar Aluno ID 1)
curl -X PATCH %BASE_URL%/alunos/1/ativar
echo.
echo ---------------------------------------------------

echo [8/9] GET /estatisticas - (Obter Estatisticas)
curl -X GET %BASE_URL%/estatisticas
echo.
echo ---------------------------------------------------

echo [9/9] DELETE /alunos/1 - (Excluir Aluno ID 1)
curl -X DELETE %BASE_URL%/alunos/1
echo.
echo ---------------------------------------------------

echo ===================================================
echo TESTES CONCLUIDOS
echo ===================================================
pause