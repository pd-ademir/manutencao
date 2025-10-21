from sqlalchemy import create_engine, text

# Certifique-se de que esse caminho é o correto
engine = create_engine("sqlite:///instance/checklist.sqlite3")

with engine.connect() as conn:
    try:
        conn.execute(text("DELETE FROM checklist"))
        conn.commit()
        print("🧹 Todos os dados da tabela checklist foram apagados com sucesso.")
    except Exception as e:
        print("⚠️ Erro ao apagar os dados:")
        print(e)
