import openai
import json
import pdfplumber
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse  
import pyngrok
import pyngrok.ngrok
import uvicorn
import pyperclip



app = FastAPI()
env = json.load(open("env.json"))

origins = [
    
    env["ngrokUrl"],
    "https://script.google.com"
]
app.add_middleware(
    
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)
KEY = env["openAiKey"]
client = openai.OpenAI(api_key=KEY)
context = """
Considere este JSON como modelo de edital de licitação. O objetivo é preencher as informações faltantes com base no contexto fornecido, sempre incluindo as coordenadas dos trechos citados entre colchetes `"[... seção.parágrafo trecho ...]"` para que a resposta seja citável. **Cada resposta deve ter um resumo seguido do trecho exato com coordenadas entre colchetes, apenas se estas estiverem explicitamente no edital.**

IMPORTANTE:

- **Sempre inclua o resumo seguido da citação com coordenadas entre colchetes**, usando a sintaxe `resumo [... seção.parágrafo trecho ...]`. 
- **Somente preencha campos que têm informações e coordenadas explícitas no edital**. Se as coordenadas não forem indicadas no documento, o campo deve permanecer vazio ou receber “Não aplicável”.
- **Não adicione chaves ou informações extras** que não estejam no modelo JSON fornecido.

Para cada chave, siga as instruções específicas:

1. **"orgao_licitante", "data", "hora", "localidade_da_prestacao_dos_serviços", "pregao_eletronico", "uasg", "valor_do_edital"**: Preencha apenas o valor exato. Não inclua colchetes se não houver coordenadas.

2. **"site_de_disputa"**: Inclua `site` e `finalidade` conforme o JSON, sem alterações.

3. **"objeto"**: Inclua o resumo do objeto seguido do trecho e coordenadas, como `Resumo do objeto [... 1.1 O objeto do presente instrumento é ...]`.

4. **"modo_de_disputa"**: Inclua a descrição completa do modo e critério de julgamento seguido da citação com coordenadas, como `Aberto [... 1.4 O pregão será do tipo menor preço ...]`.

5. **"exclusivo_para_epp/me", "subcontratacao", "consorcio"**: Use `Sim` ou `Não` seguido da citação e coordenadas, como `Sim [... 3.1 A licitação é exclusiva para microempresas ...]`.

6. **"registro_junto_a_orgaos_de_fiscalizacao"**: Inclua um resumo especificando os órgãos e suas funções, seguido da citação completa com coordenadas; se não aplicável, use `"Não aplicável [... seção.parágrafo ...]"`. Exemplo: `Registro no CREA, Vigilância Sanitária e Corpo de Bombeiros, conforme a natureza do serviço [... 4.3 Registro no CREA, Vigilância Sanitária ...]`.

7. **"clausula_adesao"**: Inclua se o edital prevê cláusula de adesão e a citação completa com coordenadas, como `O edital prevê cláusula de adesão [... 6.3 O edital prevê que os licitantes devem aderir ...]`.

8. **"vigencia_do_contrato", "permite_prorrogacao"**: Indique o resumo de vigência ou prazo seguido da citação e coordenadas, como `12 meses [... 1.2 O prazo de vigência do contrato será de 12 meses ...]`.

9. **"criterio_de_julgamento", "garantia_contratual"**: Inclua o critério ou valor seguido da citação com coordenadas, como `Menor preço [... 1.5 O critério será o menor preço unitário ...]`.

10. **"exigencia_de_visita_tecnica", "garantia_contratual_antes_da_disputa", "necessario_entrega_de_amostra", "necessario_ter_filial_no_local"**: Use `Sim` ou `Não`, seguido da citação com coordenadas, se aplicável.

11. **"qualificacao_tecnica_atestados"**: Resuma as qualificações e registros exigidos. Se aplicável, adicione a citação com coordenadas. Exemplo: `O licitante deve apresentar atestados de capacidade técnica que comprovem experiência em serviços similares e conhecimentos locais [... 4.4 O licitante deve comprovar ...]`.

12. **"prazo_para_impugnacao_e_pedido_de_esclarecimentos"**: Inclua a data e a citação completa com coordenadas, como `Até 3 dias úteis antes [... 4.7 O prazo para esclarecimentos ...]`.

13. **"desclassificacao_das_propostas"**: Forneça um resumo dos critérios que podem levar à desclassificação, como valores inexequíveis ou falta de documentação, seguido do trecho completo e coordenadas. Exemplo: `Propostas serão desclassificadas por descumprimento técnico, valores inexequíveis ou documentação incompleta [... 6.2 As propostas podem ser desclassificadas ...]`.

14. **"do_recurso"**: Descreva o prazo e processo de recurso seguido da citação com coordenadas, como `Prazo de 3 dias úteis [... 6.1 O edital prevê que o recurso deverá ...]`.

15. **"analise_juridica"**: Inclua uma análise jurídica com uma conclusão direta sobre a conformidade do edital e a necessidade de esclarecimentos ou impugnações. A análise deve seguir o exemplo: `Após análise das cláusulas contratuais do edital e dos documentos enviados, foi verificado que estão em conformidade com a Lei nº 14.133/2021. Não há necessidade de solicitar esclarecimentos, pois todas as cláusulas estão de acordo com as exigências legais e regulamentares da nova Lei de Licitações .`


### Exemplo de JSON preenchido:

{
    "orgao_licitante": "TJ - Tribunal de Justiça do Estado",
    "data": "25/10/2024",
    "hora": "10:00",
    "localidade_da_prestacao_dos_serviços": "Rua Líbero Badaró, N 600, Centro, São Paulo - SP",
    "site_de_disputa": [
        {
           "site": "https://www.gov.br/editais",
           "finalidade": "Publicação do edital"  
        }, 
        {
            "site": "https://www.gov.br/compras",
            "finalidade": "Envio de propostas e lances"
        }
    ],
    "objeto": "Locação de máquinas de bebidas quentes [... 1.1 O objeto do presente instrumento é a contratação de serviços de locação de 17 máquinas de bebidas quentes ...]",
    "pregao_eletronico": "90019/2024",
    "uasg": "380193",
    "valor_do_edital": "R$ 277.500,00",
    "modo_de_disputa": "Aberto [... 1.4 O critério de julgamento será pelo menor preço ...]",
    "exclusivo_para_epp/me": "Não [... 3.1 A empresa não deverá ser uma microempresa ou empresa de pequeno porte ...]",
    "subcontratacao": "Não [... 1.8 O contratado não poderá subcontratar ...]",
    "consorcio": "Não [... 3.6 Não é permitida a participação em consórcio ...]",
    "registro_junto_a_orgaos_de_fiscalizacao": "Registro no CREA, Vigilância Sanitária e Corpo de Bombeiros, conforme o tipo de serviço [... 4.3 Registro exigido no CREA, Vigilância Sanitária e Corpo de Bombeiros ...]",
    "clausula_adesao": "Não [... 6.3 O edital não prevê cláusula de adesão ...]",
    "vigencia_do_contrato": "15 meses [... 1.2 O prazo de vigência do contrato é de 15 meses contados da assinatura do contrato ...]",
    "permite_prorrogacao": "Sim [... 1.3 A prorrogação deverá ocorrer mediante termo aditivo ...]",
    "criterio_de_julgamento": "Menor preço [... 1.5 O critério de julgamento será o menor preço por item, realizado por meio de sistema eletrônico ...]",
    "garantia_contratual": "Não [... 3.5 Não haverá exigência de garantia contratual ...]",
    "exigencia_de_visita_tecnica": "Não [... 4.2 A vistoria não é necessária ...]",
    "garantia_contratual_antes_da_disputa": "Não [... 3.5 Não há exigência de garantia antes da disputa ...]",
    "necessario_entrega_de_amostra": "Não [... 4.4 Não são exigidas amostras para esse processo ...]",
    "necessario_ter_filial_no_local": "Não [... seção.parágrafo ...]",
    "qualificacao_tecnica_atestados": "Atestados de experiência comprovada e conhecimento técnico específico [... 4.3 O licitante deve comprovar conhecimento prévio ...]",
    "prazo_para_impugnacao_e_pedido_de_esclarecimentos": "Até 3 dias úteis antes [... 4.7 Os interessados devem protocolar impugnação ...]",
    "desclassificacao_das_propostas": "Propostas serão desclassificadas por descumprimento técnico, valores inexequíveis ou documentação incompleta [... 6.2 As propostas podem ser desclassificadas se não atenderem às especificações ...]",
    "do_recurso": "Prazo de 15 dias [... 6.1 Da decisão cabe recurso no prazo de 15 dias úteis contando da intimação ...]",
    "analise_juridica": "Após análise das cláusulas contratuais do edital e dos documentos enviados, foi verificado que estão em conformidade com a Lei nº 14.133/2021. Não há necessidade de solicitar esclarecimentos, pois todas as cláusulas estão de acordo com as exigências"
}


"""

def split_pdf(file: UploadFile, size_of_split: int = 4000) -> list:
    pdf = pdfplumber.open(file.file)
    complete_text = ""
    
    for page in pdf.pages:
        complete_text += page.extract_text()
    
    # Divida o texto em partes de até size_of_split, garantindo que palavras não sejam cortadas
    split_text = []
    while len(complete_text) > size_of_split:
        # Encontre o último espaço antes do limite de size_of_split
        split_point = complete_text.rfind(' ', 0, size_of_split)
        if split_point == -1:
            split_point = size_of_split  # Se não houver espaço, divida no limite
        split_text.append(complete_text[:split_point])
        complete_text = complete_text[split_point:].lstrip()  # Remova espaços em branco à esquerda
    
    # Adicione o texto restante
    if complete_text:
        split_text.append(complete_text)
    
    return split_text

def add_messages(messages: list, message: str) -> list[dict[str, str]]:
    
    if messages.__len__() == 0:
        raise Exception("messages is empty")
    

    messages.append({"role": "user", "content": message})
    
    return messages

def extract_json_from_response(response: openai.ChatCompletion) -> dict:
    try:
        # Extrair o conteúdo entre as chaves '{' e '}'
        content = response.choices[0].message.content
        json_str = "{" + content.split("{", 1)[1].rsplit("}", 1)[0] + "}"
        return json.loads(json_str)
    except (IndexError, ValueError, json.JSONDecodeError) as e:
        
        print (response.choices[0].message.content)
        print(f"Erro ao extrair JSON: {e}")
        return None

def ask(list_answers: list[str]) -> dict[str, str]:
    
    system_message = {
        "role": "system",
        "content": context
    }
    messages =[
        
        system_message
    ]
    for answer in list_answers:
        messages = add_messages(messages, answer)
   
    
    response = client.chat.completions.create(       
        model="gpt-4o-mini",
        messages=messages,

              
   )
   
    return extract_json_from_response(response)
 

@app.post("/uploadfile/")
async def full_text_endpoint(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    
    try:
        split_text = split_pdf(file)
        json_result = ask(split_text)
        response = JSONResponse(content=json_result)
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    except Exception as e:
        response = JSONResponse(status_code=500, content={"error": str(e)})
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response


def start_ngrok(port):
    http_tunnel = pyngrok.ngrok.connect(port, "http", hostname="boss-squirrel-instantly.ngrok-free.app")
    print("URL do túnel:", http_tunnel.public_url)
    pyperclip.copy(http_tunnel.public_url)
    return http_tunnel



if __name__ == "__main__":

    port = 8000  # Porta onde o FastAPI irá rodar
    tunnel = start_ngrok(port)
    try:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=port)
    finally:
        pyngrok.ngrok.disconnect(tunnel.public_url)

  