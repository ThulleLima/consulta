import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title='CONSULTA', page_icon='📃', layout="wide")

df = pd.read_csv('THU.csv')


# Criar a interface do Streamlit
st.title("CONSULTA DE DADOS - CNAE & SERVIÇO")

# Criar abas
tab1, tab2 = st.tabs(["CNAE", "Serviço"])

with tab1:
    st.subheader("🗃️ Tabela de CNAE")
    search_cnae = st.text_input("Pesquisar por CNAE ou Descrição")

    filtered_cnae = df[["CÓDIGO CNAE", "LINK CNAE",
                        "DESCRIÇÃO CNAE"]].drop_duplicates()
    if search_cnae:
        filtered_cnae = filtered_cnae[
            filtered_cnae.apply(lambda row: row.astype(str).str.contains(
                search_cnae, case=False, na=False).any(), axis=1)
        ]

    # Criar coluna com ícone clicável para abrir link em nova guia
    filtered_cnae["🔗"] = filtered_cnae["LINK CNAE"].apply(
        lambda link: f'<a href="{link}" target="_blank">🔗</a>' if pd.notna(link) else "")
    filtered_cnae = filtered_cnae[["CÓDIGO CNAE", "🔗", "DESCRIÇÃO CNAE"]]

    st.write(filtered_cnae.to_html(escape=False, index=False).replace('<th>', '<th style="text-align:center">'), unsafe_allow_html=True)
with tab2:
    st.subheader("🛠️ Tabela de Serviço")
    search_service = st.text_input(
        "Pesquisar por Código, Descrição ou Local de Recolhimento")

    filtered_service = df[["CÓDIGO SERVIÇO",
                           "DESCRIÇÃO SERVIÇO", "LOCAL DE RECOLHIMENTO - ISS"]]
    if search_service:
        filtered_service = filtered_service[
            filtered_service.apply(lambda row: row.astype(str).str.contains(
                search_service, case=False, na=False).any(), axis=1)
        ]

    st.table(filtered_service)  # Usa st.table() para ajustar melhor o texto

st.write("© 2025 - Desenvolvido por [Thulle Lima]")
