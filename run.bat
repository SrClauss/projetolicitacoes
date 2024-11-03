@echo off
REM Ativar o ambiente virtual
call venv\Scripts\activate

REM Executar o script main.py
python main.py

REM Desativar o ambiente virtual após a execução
deactivate