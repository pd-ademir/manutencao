import sqlite3

caminho_banco = r"C:\Users\Transp - Ornilio\Downloads\python\manutencao\instance\db.sqlite3"

conn = sqlite3.connect(caminho_banco)
cursor = conn.cursor()

colunas_para_adicionar = {
    "data_ultima_revisao_preventiva": "TEXT",
    "data_ultima_revisao_intermediaria": "TEXT",
    "data_troca_oleo_diferencial": "TEXT",
    "data_troca_oleo_cambio": "TEXT",
    "data_proxima_calibragem": "TEXT"
}

for nome_coluna, tipo in colunas_para_adicionar.items():
    try:
        cursor.execute(f"ALTER TABLE veiculo ADD COLUMN {nome_coluna} {tipo};")
        print(f"✅ Coluna '{nome_coluna}' adicionada com sucesso!")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print(f"ℹ️ A coluna '{nome_coluna}' já existe.")
        else:
            print(f"❌ Erro ao adicionar coluna '{nome_coluna}':", e)

conn.commit()
conn.close()
