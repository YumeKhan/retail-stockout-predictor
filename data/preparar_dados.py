import sqlite3
import pandas as pd
import os

print("Iniciando a extração e preparação dos dados...")

# Pega o caminho correto da pasta data
caminho_atual = os.path.dirname(os.path.abspath(__file__))
caminho_banco = os.path.join(caminho_atual, 'retail_data.db')

conexao = sqlite3.connect(caminho_banco)

# Extração (SQL)
query = """
    SELECT 
        v.data, 
        p.nome as produto, 
        p.categoria, 
        p.preco, 
        v.quantidade_vendida
    FROM vendas v
    JOIN produtos p ON v.produto_id = p.id
"""
df_vendas = pd.read_sql_query(query, conexao)
conexao.close()

print("Dados extraídos com sucesso. Iniciando transformação...")

# Transformação (Pandas)
df_vendas['data'] = pd.to_datetime(df_vendas['data'])
df_vendas['dia_da_semana'] = df_vendas['data'].dt.day_name()
df_vendas['dia_do_mes'] = df_vendas['data'].dt.day
df_vendas['fim_de_semana'] = df_vendas['dia_da_semana'].isin(['Saturday', 'Sunday']).astype(int)

# Agrupando as vendas por dia
df_agrupado = df_vendas.groupby(['data', 'produto', 'dia_da_semana', 'dia_do_mes', 'fim_de_semana'])['quantidade_vendida'].sum().reset_index()

# Salvando o arquivo limpo
caminho_csv = os.path.join(caminho_atual, 'dados_limpos_para_ml.csv')
df_agrupado.to_csv(caminho_csv, index=False)

print(f"✅ Concluído! Dados limpos salvos em: {caminho_csv}")