@echo off
REM Defina a URL do repositório a ser clonado
set REPO_URL=https://github.com/SrClauss/projetolicitacoes

REM Defina o nome do diretório onde o repositório será clonado
set CLONE_DIR=gerador_de_relatorios

REM Criar o diretório
mkdir %CLONE_DIR%

REM Navegar até o diretório criado
cd %CLONE_DIR%

REM Clonar o repositório no diretório criado
git clone %REPO_URL% .

REM Mensagem de conclusão
echo Clonagem concluída.
pause