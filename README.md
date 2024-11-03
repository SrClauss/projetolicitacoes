# Rodando a API de Extração de Dados de Editais

Esta API, criada com FastAPI, extrai informações relevantes de editais em formato PDF e as estrutura em um JSON, utilizando o poder do modelo de linguagem GPT-4.

## Funcionalidades:

* Processamento de PDF: A API recebe um arquivo PDF de edital via upload.
* Extração de Texto: O texto do PDF é extraído e dividido em partes menores para processamento eficiente pelo GPT-4.
* Compreensão de Linguagem Natural: O GPT-4, com base em um contexto pré-definido e no texto do edital, identifica e extrai as informações-chave.
* Estruturação de Dados: As informações extraídas são organizadas em um JSON seguindo um modelo predefinido.
* Análise Jurídica: A API inclui uma análise jurídica básica sobre a conformidade do edital com a legislação vigente.

##### Tecnologia:
* Linguagem: Python
* Framework: FastAPI
* Bibliotecas: openai, pdfplumber, pyngrok, pyperclip, uvicorn
* Modelo de Linguagem: GPT-4 (OpenAI)


# Como Rodar a API:

## Configuração do Ambiente:

Certifique-se de ter o Python 3.7 ou superior instalado.
Crie um ambiente virtual (venv) e ative-o.
Instale as dependências listadas no arquivo requirements.txt.
Crie um arquivo env.json e preencha com sua chave de API do OpenAI e a URL do ngrok.
    
```
//env.json    
{
    "ngrokUrl": "<url_ngrok>"",
    "openAiKey": "<open_ai_api_key>"
}
``` 
    


## Inicialização:


Execute o arquivo main.py.
O ngrok será iniciado automaticamente, criando um túnel para a API.
A URL pública do ngrok será copiada para a área de transferência.



## Utilização:

Envie uma requisição POST para o endpoint /uploadfile/, anexando o arquivo PDF do edital.
A API retornará um JSON com as informações extraídas do edital.

## Observações:

A API está configurada para aceitar requisições de diferentes origens, incluindo a URL do ngrok e https://script.google.com.
O modelo de JSON de saída e o contexto fornecido ao GPT-4 podem ser personalizados de acordo com as necessidades específicas.

Exemplo de JSON de Saída:

{
    "orgao_licitante": "Exemplo de Órgão",
    "data": "01/01/2024",
    // ... outras informações extraídas do edital ...
}
Esta API oferece uma solução eficiente para automatizar a extração e estruturação de dados de editais, agilizando processos e fornecendo informações relevantes de forma organizada."