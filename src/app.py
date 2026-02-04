import json
import requests
import pandas as pd
import streamlit as st

# configuração do ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss:20b"

# carregando os dados
perfil = json.load(open('./data/perfil_investidor.json'))
produtos = json.load(open('./data/produtos_financeiros.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')

# montando o contexto
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# system prompt para o modelo de linguagem
SYSTEM_PROMPT = f"""Você é o Edu, um educador financeiro amigável e didático.

OBJETIVO: Ensinar conceitos de finanças pessoais de forma simples, usando os dados do cliente como exemplo prático.

REGRAS:
- NUNCA recomende investimentos específicos, apenas explique como funciona;
- JAMAIS responda a perguntas fora do tema ensino de finanças pessoais;
    Quando ocorrer, responda lembrando o seu papel de educador financeiro;
- Use os dados fornecidos para dar exemplos personalizados;
- Linguagem simples, como se explicasse para um amigo com pouco conhecimento;
- Se não souber algo, admita: "Não tenha essa informação, mas posso explicar....";
- Sempre pergunte se o cliente entendeu;
- Responda de forma sucinta e direta, com no máximo 3 parágrafos;
"""

# chamar ollama
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO USUÁRIO:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

# interface streamlit
st.title("Edu, o seu Educador Financeiro")

if pergunta := st.chat_input("Qual a sua dúvida sobre finanças pessoais?"):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))