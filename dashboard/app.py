# dashboard/app.py
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

st.title("🎬 Dashboard de Filmes")
st.write("Dashboard interativo para análise de bilheteria, gêneros e estúdios")

# Carregar dados
@st.cache_data(ttl=300)
def carregar_filmes():
    response = requests.get(f"{API_URL}/filmes")
    df = pd.DataFrame(response.json())
    df["estudios_lista"] = df["estudio"].apply(lambda x: [e.strip() for e in x.split("/")])
    # Formatar bilheteria com separador e cifrão
    df["bilheteria_formatada"] = df["bilheteria"].apply(lambda x: f"${x:,.0f}")
    return df

@st.cache_data(ttl=300)
def carregar_analise_genero():
    response = requests.get(f"{API_URL}/filmes/analise")
    df = pd.DataFrame(response.json())
    df["bilheteria_total_formatada"] = df["bilheteria_total"].apply(lambda x: f"${x:,.0f}")
    return df

@st.cache_data(ttl=300)
def carregar_analise_estudio():
    response = requests.get(f"{API_URL}/filmes/analise_estudios")
    df = pd.DataFrame(response.json())
    df["bilheteria_total_formatada"] = df["bilheteria_total"].apply(lambda x: f"${x:,.0f}")
    df["bilheteria_media_formatada"] = df["bilheteria_media"].apply(lambda x: f"${x:,.0f}")
    return df

# Inserir filme
def inserir_filme(dados):
    response = requests.post(f"{API_URL}/filmes", json=dados)
    return response.status_code in [200, 201]

try:
    df_filmes = carregar_filmes()
    df_analise_genero = carregar_analise_genero()
    df_analise_estudio = carregar_analise_estudio()

    # FILTROS
    st.sidebar.subheader("🎛️ Filtros")
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

    tab1, tab2 = st.tabs(["📊 Visualização de Dados", "➕ Inserir Novo Filme"])

    with tab1:
        # Mostrar primeiro a lista de filmes
        st.subheader("🎥 Filmes Filtrados")
        st.dataframe(df_filtrado.drop(columns=["estudios_lista", "bilheteria"]))

        col1, col2 = st.columns(2)

        # Gráfico bilheteria total por gênero
        with col1:
            st.subheader("Bilheteria Total por Gênero")
            fig1 = px.bar(
                df_analise_genero,
                x="genero",
                y="bilheteria_total",
                text=df_analise_genero["bilheteria_total"].apply(lambda x: f"${x:,.0f}"),
                color="genero",
                title="Bilheteria Total por Gênero",
                height=400
            )
            fig1.update_traces(showlegend=False, textposition="outside")
            fig1.update_layout(xaxis_title="", yaxis_title="")
            st.plotly_chart(fig1, use_container_width=True)

        # Gráfico distribuição de filmes por gênero
        with col2:
            st.subheader("Distribuição de Filmes por Gênero")
            fig2 = px.pie(
                df_analise_genero,
                values="total_filmes",
                names="genero",
                title="Distribuição de Filmes por Gênero"
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Gráficos de estúdio
        st.subheader("Bilheteria por Estúdio")
        df_estudio_plot = df_analise_estudio.sort_values("bilheteria_total", ascending=False)

        col3, col4 = st.columns(2)

        # Bilheteria Total
        with col3:
            fig3 = px.bar(
                df_estudio_plot,
                y="estudio",
                x="bilheteria_total",
                orientation="h",
                title="Bilheteria Total por Estúdio",
                text=df_estudio_plot["bilheteria_total"].apply(lambda x: f"${x:,.0f}"),
                height=400
            )
            fig3.update_traces(textposition="outside", showlegend=False)
            fig3.update_layout(yaxis={"categoryorder": "total ascending"}, xaxis_title="", yaxis_title="")
            st.plotly_chart(fig3, use_container_width=True)

        # Bilheteria Média
        with col4:
            fig4 = px.bar(
                df_estudio_plot,
                y="estudio",
                x="bilheteria_media",
                orientation="h",
                title="Bilheteria Média por Estúdio",
                text=df_estudio_plot["bilheteria_media"].apply(lambda x: f"${x:,.0f}"),
                height=400
            )
            fig4.update_traces(textposition="outside", showlegend=False)
            fig4.update_layout(yaxis={"categoryorder": "total ascending"}, xaxis_title="", yaxis_title="")
            st.plotly_chart(fig4, use_container_width=True)

    # Aba de inserção
    with tab2:
        st.subheader("Adicionar Novo Filme")
        with st.form("novo_filme_form"):
            titulo = st.text_input("Título do Filme")
            diretor = st.text_input("Diretor")
            estudio = st.text_input("Estúdio(s) (separe múltiplos por /)")
            genero = st.text_input("Gênero")
            ano_lancamento = st.number_input("Ano de Lançamento", min_value=1900, max_value=2100, step=1)
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
                        "ano_lancamento": ano_lancamento,
                        "bilheteria": bilheteria
                    }
                    if inserir_filme(novo_filme):
                        st.success("Filme adicionado com sucesso! 🎉")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("Erro ao adicionar filme. Verifique os dados e tente novamente.")

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.warning("Verifique se a API está disponível e funcionando corretamente.")
