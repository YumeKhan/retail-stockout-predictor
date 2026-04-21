import sqlite3
import random
from datetime import datetime, timedelta
import os

print("Iniciando a criação do banco de dados...")

caminho_atual = os.path.dirname(os.path.abspath(__file__))
caminho_banco = os.path.join(caminho_atual, 'retail_data.db')

conexao = sqlite3.connect(caminho_banco)
cursor = conexao.cursor()

# ⚠️ A SOLUÇÃO: Destruir as tabelas velhas antes de criar novas para zerar os IDs
cursor.execute('DROP TABLE IF EXISTS vendas')
cursor.execute('DROP TABLE IF EXISTS produtos')

# Recriando as tabelas limpinhas
cursor.execute('''CREATE TABLE produtos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, categoria TEXT, preco REAL)''')
cursor.execute('''CREATE TABLE vendas (id INTEGER PRIMARY KEY AUTOINCREMENT, produto_id INTEGER, data DATE, quantidade_vendida INTEGER, FOREIGN KEY (produto_id) REFERENCES produtos (id))''')

# Inserindo Produtos (Eles terão IDs de 1 a 5 com certeza agora)
produtos_lista = [
    ('Dipirona 500mg', 'Medicamentos', 5.99), 
    ('Vitamina C 1g', 'Suplementos', 25.50), 
    ('Shampoo Anticaspa', 'Higiene', 18.90), 
    ('Fralda Descartável P', 'Infantil', 45.00), 
    ('Protetor Solar FPS 50', 'Cosméticos', 60.00)
]
cursor.executemany('INSERT INTO produtos (nome, categoria, preco) VALUES (?, ?, ?)', produtos_lista)

# Inserindo Vendas
data_hoje = datetime.now()
data_inicial = data_hoje - timedelta(days=30)
vendas_lista = []

for _ in range(500):
    produto_id = random.randint(1, 5) # Agora vai bater perfeitamente!
    dias_aleatorios = random.randint(0, 30)
    data_venda = data_inicial + timedelta(days=dias_aleatorios)
    quantidade = random.randint(1, 15)
    vendas_lista.append((produto_id, data_venda.strftime('%Y-%m-%d'), quantidade))

cursor.executemany('INSERT INTO vendas (produto_id, data, quantidade_vendida) VALUES (?, ?, ?)', vendas_lista)
conexao.commit()
conexao.close()

print(f"✅ Sucesso! O arquivo 'retail_data.db' foi gerado e os IDs foram resetados!")