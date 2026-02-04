# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores |
| `transacoes.csv` | CSV | Analisar padrão de gastos |
| `perfil_investidor.json` | JSON | Personalizar recomendações |
| `produtos_financeiros.json` | JSON | Sugerir produtos adequados ao perfil |

---

## Estratégia de Integração

### Como os dados são carregados?
```
import json
import pandas as pd

perfil = json.load(open('./data/perfil_investidor.json'))
produtos = json.load(open('./data/produtos_financeiros.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
```

### Como os dados são usados no prompt?
No código, o SYSTEM_PROMPT contém apenas as regras de comportamento, a personalidade do "Edu" e as diretrizes de segurança (o que ele pode ou não fazer).

Os dados do cliente (perfil, transações e produtos) estão sendo colocados em uma variável separada chamada `contexto`. Na função `perguntar(msg)`, você concatena tudo:
1. O System Prompt (Regras)
2. O Contexto (Dados dos arquivos JSON/CSV na pasta data)
3. Sua pergunta

Sendo consultados dinamicamente e a cada execução do script, os dados tem o seguinte fluxo:
- **Carga Inicial:** Quando você inicia o app, o Pandas e o json.load leem os arquivos (transacoes.csv, etc.).
- **Montagem do Contexto:** O código transforma esses dados em texto (to_string() e json.dumps()).
- **Envio no Prompt:** Toda vez que você faz uma pergunta no Chat Input do Streamlit, o seu código pega a foto "atual" desses dados e envia para o modelo.

---

## Exemplo de Contexto Montado

```
Dados do Cliente:
- Nome: Bruno
- Perfil: Seguro
- Saldo disponível: R$ 200
- Objetivo principal: Montar patrimônio
...

Últimas transações:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55
...
```
