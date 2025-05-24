import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title='CONSULTA', page_icon='📃', layout="wide")

# Carregar CSV com tipos de dados corretos e remover valores NaN
df = pd.read_csv('THU.csv', dtype={"CÓDIGO CNAE": str, "CÓDIGO SERVIÇO": str})
df = df.fillna("")  # SUBSTITUI valores NaN por strings vazias

# Exibir logomarca
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image("logo.png", width=200,)

# Criar interface do Streamlit
st.title("CONSULTA DE DADOS - CNAE & SERVIÇO")

# Criar abas
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Home","CNAE", "Serviço", "Gerenciar CNAE","Gerenciar Serviço","Calculadora IR/INSS"])

# 🔹 Aba 1: Home
with tab1:
    st.title("Olá! Bem vindo!")
    st.subheader("Esta é uma página dedicada à consulta de dados referentes serviços e tributações.")
    
    st.write("Aqui você irá encontrar:")
    st.write("🔸Tabela de consulta para CNAE (Classificação Nacional de Atividades Econômicas)")
    st.write("🔸Tabela com códigos de serviços municipais.")
    st.write("🔸Editor das tabelas real time, que permite atualização facilitada dos dados.")
    st.write("🔸Calculadora de IR e INSS à recolher para pessoa física.")

# 🔹 Aba 2: Tabela CNAE
with tab2:
    st.subheader("🗃️ Tabela de CNAE")
    search_cnae = st.text_input("Pesquisar por CNAE ou Descrição")

    filtered_cnae = df[["CÓDIGO CNAE", "LINK CNAE", "DESCRIÇÃO CNAE"]].drop_duplicates()
    if search_cnae:
        filtered_cnae = filtered_cnae[
            filtered_cnae.apply(lambda row: row.astype(str).str.contains(
                search_cnae, case=False, na=False).any(), axis=1)
        ]

    # Criar coluna com ícone clicável para abrir link
    filtered_cnae["🔗"] = filtered_cnae["LINK CNAE"].apply(
        lambda link: f'<a href="{link}" target="_blank">🔗</a>' if pd.notna(link) else "")
    filtered_cnae = filtered_cnae[["CÓDIGO CNAE", "🔗", "DESCRIÇÃO CNAE"]]

    st.write(filtered_cnae.to_html(escape=False, index=False).replace('<th>', '<th style="text-align:center">'), unsafe_allow_html=True)

# 🔹 Aba 3: Tabela de Serviços
with tab3:
    st.subheader("🛠️ Tabela de Serviço")
    search_service = st.text_input("Pesquisar por Código, Descrição ou Local de Recolhimento")

    filtered_service = df[["CÓDIGO SERVIÇO", "DESCRIÇÃO SERVIÇO", "LOCAL DE RECOLHIMENTO - ISS"]]
    if search_service:
        filtered_service = filtered_service[
            filtered_service.apply(lambda row: row.astype(str).str.contains(
                search_service, case=False, na=False).any(), axis=1)
        ]
    st.write(filtered_service.to_html(escape=False, index=False).replace('<th>', '<th style="text-align:center">'), unsafe_allow_html=True)  # Usa st.table() para ajustar melhor o texto

# 🔹 Aba 4: Gerenciar CNAE (Adicionar, Editar e Remover)
with tab4:
    st.subheader("➕ CNAE")

    # 🔸 Adicionar novo CNAE
    st.write("")
    st.write("### Adicionar Novo CNAE")
    new_cnae = st.text_input("Código CNAE")
    new_link = st.text_input("Link CNAE")
    new_desc = st.text_input("Descrição CNAE")

    if st.button("Adicionar CNAE", key='add_cnae'):
        if new_cnae and new_desc:
            new_row = pd.DataFrame({"CÓDIGO CNAE": [new_cnae], "LINK CNAE": [new_link], "DESCRIÇÃO CNAE": [new_desc]})
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv('THU.csv', index=False)
            st.success("Novo CNAE adicionado com sucesso!")
            st.rerun()
        else:
            st.error("Por favor, preencha todos os campos obrigatórios!")

    # 🔸 Editar e Remover CNAEs
    st.write("### Editar ou Remover CNAE")
    selected_cnae = st.selectbox("Selecione um CNAE para editar/remover", df["CÓDIGO CNAE"].unique())

    if selected_cnae:
        # Filtrar o CNAE selecionado
        selected_row = df[df["CÓDIGO CNAE"] == selected_cnae].iloc[0]
        
        edit_cnae = st.text_input("Editar Código CNAE", value=selected_row["CÓDIGO CNAE"])
        edit_link = st.text_input("Editar Link CNAE", value=selected_row["LINK CNAE"])
        edit_desc = st.text_input("Editar Descrição CNAE", value=selected_row["DESCRIÇÃO CNAE"])

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Salvar Alterações", key="save_cnae"):
                df.loc[df["CÓDIGO CNAE"] == selected_cnae, ["CÓDIGO CNAE", "LINK CNAE", "DESCRIÇÃO CNAE"]] = [edit_cnae, edit_link, edit_desc]
                df.to_csv('THU.csv', index=False)
                st.success("CNAE atualizado com sucesso!")
                st.rerun()
        
        with col2:
            if st.button("Remover CNAE", key="remove_cnae"):
                df = df[df["CÓDIGO CNAE"] != selected_cnae]  # Remove a linha selecionada
                df.to_csv('THU.csv', index=False)
                st.success("CNAE removido!")
                st.rerun()

# 🔹 Aba 5: Gerenciar Serviço (Adicionar, Editar e Remover)
with tab5:
    st.subheader("➕Códigos de Serviço")

    # 🔸 Adicionar novo CNAE
    st.write("")
    st.write("### Adicionar Novo Serviço")
    new_serv = st.text_input("Código Serviço") 
    new_desc2 = st.text_input("Descrição do Serviço") 
    new_local = st.text_input("Local de recolhimento do ISS") 

    if st.button("Adicionar novo Serviço", key='add_serv'):
        if new_serv and new_local:
            new_row2 = pd.DataFrame({"CÓDIGO SERVIÇO": [new_serv], "DESCRIÇÃO SERVIÇO": [new_desc2], "LOCAL DE RECOLHIMENTO - ISS": [new_local]})
            df = pd.concat([df, new_row2], ignore_index=True)
            df.to_csv('THU.csv', index=False)
            st.success("Novo CNAE adicionado com sucesso!")
            st.rerun()
        else:
            st.error("Por favor, preencha todos os campos obrigatórios!")

    # 🔸 Editar e Remover CNAEs
    st.write("### Editar ou Remover Serviço")
    selected_serv = st.selectbox("Selecione um Serviço para editar/remover", df["CÓDIGO SERVIÇO"].unique()) 

    if selected_serv:
        # Filtrar o CNAE selecionado
        selected_row2 = df[df["CÓDIGO SERVIÇO"] == selected_serv].iloc[0]
        
        edit_cod = st.text_input("Editar Código de Serviço", value=selected_row2["CÓDIGO SERVIÇO"])
        edit_desc2 = st.text_input("Editar Descrição do Serviço", value=selected_row2["DESCRIÇÃO SERVIÇO"])
        edit_iss = st.text_input("Editar Local de recolhimento do ISS", value=selected_row2["LOCAL DE RECOLHIMENTO - ISS"])

        col1, col2 = st.columns(2)
        with col1:
           if st.button("Salvar Alterações", key="save_service"):
                df.loc[df["CÓDIGO SERVIÇO"] == selected_serv, ["CÓDIGO SERVIÇO", "DESCRIÇÃO SERVIÇO", "LOCAL DE RECOLHIMENTO - ISS"]] = [edit_cod, edit_desc2, edit_iss]
                df.to_csv('THU.csv', index=False)
                st.success("Serviço atualizado com sucesso!")
                st.rerun()
        
        with col2:
            if st.button("Remover Serviço", key="remove_service"):
                df = df[df["CÓDIGO SERVIÇO"] != selected_serv]  # Remove a linha selecionada
                df.to_csv('THU.csv', index=False)
                st.warning("Serviço removido!")
                st.rerun()

# 🔹 Aba 6: Calculadora PF
with tab6:
    st.subheader("🧮Calculadora IR/INSS pessoa física")

    colE, colC, colD = st.columns(3)
    with colE:
        st.markdown("")
    with colC:
        st.image("tabela.png", use_column_width=True,caption="Valores utilizados como referência")
    with colE:
        st.markdown("")

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

st.write("© 2025 - Desenvolvido com 🧡 por [Thulle Lima]",)
