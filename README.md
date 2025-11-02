# Dashboard Clima & Energia - Comparativo

Este projeto apresenta um dashboard interativo desenvolvido com Streamlit para análise de dados de temperatura média e consumo de energia elétrica na cidade de São Paulo, no período de janeiro a junho.

## Funcionalidades
- Visualização dos dados mensais de temperatura e consumo de energia.
- Gráficos interativos para análise individual e comparativa dos indicadores.
- Métricas automáticas de médias e variação percentual do consumo.

## Tecnologias Utilizadas
- Python 3.8+
- Streamlit
- Pandas
- Plotly

## Estrutura do Projeto
```
app.py
requirements.txt
Dockerfile
README.md
```

## Como Executar Localmente
1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Execute o aplicativo Streamlit:**
   ```bash
   streamlit run app.py
   ```
3. **Acesse o dashboard:**
   Abra o navegador e acesse o endereço exibido pelo Streamlit (geralmente http://localhost:8501).

## Executando com Docker
1. **Construa a imagem:**
   ```bash
   docker build -t dashboard-clima-energia .
   ```
2. **Execute o container:**
   ```bash
   docker run -p 8501:8501 dashboard-clima-energia
   ```
3. **Acesse o dashboard:**
   http://localhost:8501

## Gráficos Disponíveis
- **Temperatura Média Mensal:** Linha mostrando a variação da temperatura ao longo dos meses.
- **Consumo de Energia Mensal:** Linha mostrando o consumo de energia mês a mês.
- **Comparativo:** Gráfico com dois eixos para visualizar simultaneamente temperatura e consumo.

## Métricas Apresentadas
- Média de temperatura no período.
- Média de consumo de energia no período.
- Variação percentual do consumo entre o primeiro e o último mês.

## Autor
Felipe Viana

---
Projeto para estudos e demonstração de visualização de dados com Streamlit e Plotly.
