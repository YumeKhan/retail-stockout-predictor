from fastapi import FastAPI
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import os

app = FastAPI(
    title="Retail Stockout Predictor API",
    description="API preditiva para risco de ruptura de estoque no varejo.",
    version="1.0.0"
)

# Variável global para armazenar nosso modelo de Machine Learning
modelo_ml = None

@app.on_event("startup")
def treinar_modelo():
    """Treina o modelo automaticamente quando a API é iniciada."""
    global modelo_ml
    print("⏳ Carregando dados limpos e treinando o modelo...")
    
    # Navega até a pasta data para pegar o arquivo gerado na etapa anterior
    caminho_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_dados = os.path.join(caminho_base, 'data', 'dados_limpos_para_ml.csv')
    
    try:
        df = pd.read_csv(caminho_dados)
        
        # Engenharia de Features: Criando o "Alvo" da nossa IA
        # Se um produto vende mais de 10 unidades em um dia, consideramos "Alta Demanda" (Risco de Ruptura)
        df['alta_demanda'] = (df['quantidade_vendida'] > 10).astype(int)
        
        # Separando o que a IA vai usar para aprender (X) e o que ela tem que prever (y)
        X = df[['dia_do_mes', 'fim_de_semana']] 
        y = df['alta_demanda']
        
        # Treinando um algoritmo de Árvore de Decisão Avançada (Random Forest)
        modelo_ml = RandomForestClassifier(n_estimators=50, random_state=42)
        modelo_ml.fit(X, y)
        print("✅ Modelo treinado com sucesso! API pronta para uso.")
        
    except FileNotFoundError:
        print("❌ Erro: O arquivo 'dados_limpos_para_ml.csv' não foi encontrado. Rode o script preparar_dados.py primeiro.")

@app.get("/")
def home():
    return {"mensagem": "API do Stockout Predictor rodando! Acesse /docs para a interface interativa."}

@app.get("/prever/")
def prever_ruptura(dia_do_mes: int, fim_de_semana: int):
    """
    Informa os dados do dia para prever se haverá um pico de demanda (Risco de Esgotar).
    - dia_do_mes: 1 a 31
    - fim_de_semana: 1 (Sim) ou 0 (Não)
    """
    if modelo_ml is None:
        return {"erro": "O modelo não está disponível."}
        
    # Pedindo para a IA fazer a previsão
    previsao = modelo_ml.predict([[dia_do_mes, fim_de_semana]])
    probabilidade = modelo_ml.predict_proba([[dia_do_mes, fim_de_semana]])[0][1]
    
    risco = "ALTO RISCO (Estoque pode zerar)" if previsao[0] == 1 else "BAIXO RISCO"
    
    return {
        "parametros_recebidos": {"dia_do_mes": dia_do_mes, "fim_de_semana": bool(fim_de_semana)},
        "diagnostico_ia": risco,
        "probabilidade_de_pico": f"{probabilidade * 100:.1f}%"
    }