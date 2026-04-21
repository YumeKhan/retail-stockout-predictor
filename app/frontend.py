import streamlit as st
import requests

# Configuração inicial da página
st.set_page_config(page_title="Previsor de Estoque", page_icon="🛒", layout="centered")

# Cabeçalho
st.title("🛒 Previsor de Ruptura de Estoque")
st.markdown("""
Bem-vindo ao painel gerencial! 
Esta interface se conecta em tempo real com a nossa Inteligência Artificial para prever se um produto corre risco de esgotar na farmácia.
""")
st.divider()

# Criando a interface de entrada (Inputs) em colunas para ficar bonito
col1, col2 = st.columns(2)

with col1:
    # Um slider deslizante para o dia do mês
    dia_escolhido = st.slider("Selecione o Dia do Mês:", min_value=1, max_value=31, value=15)

with col2:
    # Um botão de múltipla escolha para o fim de semana
    fim_de_semana_texto = st.radio("Cai em um fim de semana?", options=["Não", "Sim"])
    # Convertendo o texto "Sim/Não" para o 1 e 0 que a nossa API entende
    fim_semana_codificado = 1 if fim_de_semana_texto == "Sim" else 0

st.divider()

# O Botão de Ação
if st.button("🤖 Perguntar à IA", type="primary", use_container_width=True):
    
    # Esta é a URL exata da sua API do FastAPI que testamos antes
    url_api = f"http://127.0.0.1:8000/prever/?dia_do_mes={dia_escolhido}&fim_de_semana={fim_semana_codificado}"
    
    # Mostra um "carregando" enquanto vai buscar a resposta
    with st.spinner('Consultando os dados históricos e calculando previsões...'):
        try:
            # Enviando a pergunta (GET) para a API
            resposta = requests.get(url_api)
            
            if resposta.status_code == 200:
                dados = resposta.json()
                risco = dados['diagnostico_ia']
                probabilidade = dados['probabilidade_de_pico']
                
                st.subheader("Resultado da Análise:")
                
                # Mudando a cor da tela dependendo do risco
                if "ALTO" in risco:
                    st.error(f"⚠️ **{risco}**")
                    st.warning(f"Probabilidade calculada pela IA: **{probabilidade}**")
                    st.markdown("*Ação Recomendada: Acionar o setor de compras imediatamente.*")
                else:
                    st.success(f"✅ **{risco}**")
                    st.info(f"Probabilidade calculada pela IA: **{probabilidade}**")
                    st.markdown("*Ação Recomendada: Manter o fluxo normal de reposição.*")
            else:
                st.error("Ops! Tivemos um erro ao processar a resposta da API.")
                
        except requests.exceptions.ConnectionError:
            st.error("🚨 Falha de Conexão: A API não respondeu. Você lembrou de ligar o servidor do FastAPI no outro terminal?")