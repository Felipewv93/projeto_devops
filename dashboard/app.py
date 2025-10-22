import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os

API_URL = os.environ.get("API_URL", "http://api:8000")

st.set_page_config(
    page_title="Dashboard de Filmes",
    layout="wide"
)

st.title("🎬 Top 20 Maiores Bilheterias do Cinema")
st.write("Dashboard interativo para análise de bilheteria, gêneros e estúdios")

# Funções de carregamento

@st.cache_data(ttl=300)
def carregar_filmes():
    response = requests.get(f"{API_URL}/filmes")
    df = pd.DataFrame(response.json())
    df["estudios_lista"] = df["estudio"].apply(lambda x: [e.strip() for e in x.split("/")])
    return df

@st.cache_data(ttl=300)
def carregar_analise_genero():
    response = requests.get(f"{API_URL}/filmes/analise")
    return pd.DataFrame(response.json())

@st.cache_data(ttl=300)
def carregar_analise_estudio():
    response = requests.get(f"{API_URL}/filmes/analise_estudios")
    return pd.DataFrame(response.json())

# Função para formatação

def formatar_bilheteria(x):
    if x >= 1_000_000_000:
        return f"${x/1_000_000_000:.2f}B"
    elif x >= 1_000_000:
        return f"${x/1_000_000:.2f}M"
    else:
        return f"${x:,.0f}"

# Inserir filme
def inserir_filme(dados):
    response = requests.post(f"{API_URL}/filmes", json=dados)
    return response.status_code in [200, 201]

try:
    # Carregar dados

    df_filmes = carregar_filmes()
    df_analise_genero = carregar_analise_genero()
    df_analise_estudio = carregar_analise_estudio()

    # FILTROS

    st.sidebar.subheader("Filtros")
    generos = ["Todos"] + sorted(df_filmes["genero"].unique().tolist())
    genero_selecionado = st.sidebar.selectbox("Filtrar por gênero:", generos)

    todos_estudios = sorted({est for sublist in df_filmes["estudios_lista"] for est in sublist})
    estudios = ["Todos"] + todos_estudios
    estudio_selecionado = st.sidebar.selectbox("Filtrar por estúdio:", estudios)

    # Aplicar filtros
    df_filtrado = df_filmes.copy()
    if genero_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["genero"] == genero_selecionado]
    if estudio_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["estudios_lista"].apply(lambda x: estudio_selecionado in x)]

    # TABS

    tab1, tab2 = st.tabs(["Visualização de Dados", "Inserir Novo Filme"])

    with tab1:

        # Lista de filmes (primeira visualização)

        st.subheader("📽️ Filmes")
        df_mostrar = df_filtrado.drop(columns=["estudios_lista"])
        st.dataframe(df_mostrar)

        # Gráficos de gênero

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🎭 Bilheteria Total por Gênero")
            fig1 = px.bar(
                df_analise_genero,
                x="genero",
                y="bilheteria_total",
                text=df_analise_genero["bilheteria_total"].apply(formatar_bilheteria),
                color="genero",
                height=450
            )
            fig1.update_traces(textposition="outside", showlegend=False)
            fig1.update_layout(xaxis_title="", yaxis_title="")
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.subheader("🧮 Distribuição de Filmes por Gênero")
            fig2 = px.pie(
                df_analise_genero,
                values="total_filmes",
                names="genero"
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Gráficos de estúdio

        st.subheader("💲 Bilheteria por Estúdio")
        df_estudio_plot = df_analise_estudio.sort_values("bilheteria_total", ascending=False)
        col3, col4 = st.columns(2)

        with col3:
            fig3 = px.bar(
                df_estudio_plot,
                y="estudio",
                x="bilheteria_total",
                orientation="h",
                title="Bilheteria Total por Estúdio",
                text=df_estudio_plot["bilheteria_total"].apply(formatar_bilheteria),
                height=500
            )
            fig3.update_traces(textposition="inside",
            showlegend=False,
            textfont_color="black")
            fig3.update_layout(xaxis_title="",
            yaxis_title="",
            yaxis={"categoryorder": "total ascending"},
            margin_r=0)
            st.plotly_chart(fig3, use_container_width=True)

        with col4:
            fig4 = px.bar(
                df_estudio_plot,
                y="estudio",
                x="bilheteria_media",
                orientation="h",
                title="Bilheteria Média por Estúdio",
                text=df_estudio_plot["bilheteria_media"].apply(formatar_bilheteria),
                height=500
            )
            fig4.update_traces(textposition="inside", showlegend=False, textfont_color="black")
            fig4.update_layout(xaxis_title="", yaxis_title="", yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig4, use_container_width=True)

    # Aba de inserção

    with tab2:
        st.subheader("➕ Adicionar Novo Filme")
        with st.form("novo_filme_form"):
            titulo = st.text_input("Título do Filme")
            diretor = st.text_input("Diretor")
            estudio = st.text_input("Estúdio(s) (separe múltiplos por /)")
            genero = st.text_input("Gênero")
            ano = st.number_input("Ano de Lançamento", min_value=1900, max_value=2100, step=1)
            bilheteria = st.number_input("Bilheteria (USD)", min_value=0, step=1)

            submitted = st.form_submit_button("Adicionar Filme")

            if submitted:
                if not titulo or not diretor or not estudio or not genero:
                    st.error("Todos os campos são obrigatórios!")
                else:
                    novo_filme = {
                        "titulo": titulo,
                        "diretor": diretor,
                        "estudio": estudio,
                        "genero": genero,
                        "ano": ano,
                        "bilheteria": bilheteria
                    }
                    if inserir_filme(novo_filme):
                        st.success("Filme adicionado com sucesso!")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("Erro ao adicionar filme. Verifique os dados e tente novamente.")

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.warning("Verifique se a API está disponível e funcionando corretamente.")
