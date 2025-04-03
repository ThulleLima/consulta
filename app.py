import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title='CONSULTA', page_icon='📃', layout="wide")

df = pd.read_csv('THU.csv', dtype={"CÓDIGO SERVIÇO": str})

# Exibir logomarca
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image("logo.png", width=200)

# Criar a interface do Streamlit
st.title("CONSULTA DE DADOS - CNAE & SERVIÇO")

# Criar abas
tab1, tab2, tab3 = st.tabs(["CNAE", "Serviço", "Calculadora IR/INSS"])

with tab1:
    st.subheader("🗃️ Tabela de CNAE")
    search_cnae = st.text_input("Pesquisar por CNAE ou Descrição")

    filtered_cnae = df[["CÓDIGO CNAE", "LINK CNAE", "DESCRIÇÃO CNAE"]].drop_duplicates()
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
    search_service = st.text_input("Pesquisar por Código, Descrição ou Local de Recolhimento")

    filtered_service = df[["CÓDIGO SERVIÇO", "DESCRIÇÃO SERVIÇO", "LOCAL DE RECOLHIMENTO - ISS"]]
    if search_service:
        filtered_service = filtered_service[
            filtered_service.apply(lambda row: row.astype(str).str.contains(
                search_service, case=False, na=False).any(), axis=1)
        ]

    st.write(filtered_service.to_html(escape=False, index=False).replace('<th>', '<th style="text-align:center">'), unsafe_allow_html=True)

with tab3:
    st.subheader("🧮 Calculadora IR/INSS pessoa física")

    colE, colC, colD = st.columns(3)
    with colC:
        st.image("tabela.png", use_container_width=True, caption="Valores utilizados como referência")
    
    valor_servico = st.number_input("Informe o valor do serviço", min_value=0.0, format="%.2f")
    
    if valor_servico > 0:
        # Cálculo do INSS
        CINSS = valor_servico * 0.11
        CINSS = min(CINSS, 897.32)  # Limite máximo do INSS
        
        # Base de cálculo do IR
        BC = valor_servico - CINSS
        
        # Determinar alíquota e parcela dedutível
        if BC <= 2259.20:
            AL, PD = 0, 0
        elif 2259.21 <= BC <= 2826.65:
            AL, PD = 0.075, 169.44
        elif 2826.66 <= BC <= 3751.05:
            AL, PD = 0.15, 381.44
        elif 3751.06 <= BC <= 4664.68:
            AL, PD = 0.225, 662.77
        else:
            AL, PD = 0.275, 896.00
        
        # Cálculo do IR
        VBR = BC * AL
        VFIR = max(VBR - PD, 0)  # IR não pode ser negativo
        
        # Exibir resultados em destaque
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**INSS à Recolher:**")
            st.code(f"R$ {CINSS:,.2f}")
            
        with col2:
            st.markdown("**IR a Recolher:**")
            st.code(f"R$ {VFIR:,.2f}")
        
        # Script JavaScript para copiar automaticamente ao clicar no botão
        st.markdown("""
        <script>
        function copyText(text) {
            navigator.clipboard.writeText(text);
            alert("Valor copiado para a área de transferência: " + text);
        }
        </script>
        """, unsafe_allow_html=True)
   
st.write("© 2025 - Desenvolvido por [Thulle Lima]")
