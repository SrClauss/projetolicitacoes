@echo off
REM Verificar se o Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python não está instalado. Por favor, instale o Python 3.7 ou superior.
    pause
    exit /b 1
)

REM Criar o ambiente virtual
python -m venv venv

REM Ativar o ambiente virtual
call venv\Scripts\activate

REM Instalar as dependências do requirements.txt
pip install -r requirements.txt

REM Mensagem de conclusão
echo Ambiente virtual criado e dependências instaladas.
pause