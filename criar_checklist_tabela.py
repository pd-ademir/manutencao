import sqlite3

conn = sqlite3.connect("instance/checklist.sqlite3")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS checklist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mes TEXT NOT NULL,
    data_registro DATE NOT NULL,
    placa TEXT NOT NULL,
    item TEXT NOT NULL,
    fonte TEXT NOT NULL,
    tipo_manutencao TEXT NOT NULL,
    status TEXT NOT NULL,
    ordem_servico TEXT,
    conclusao TEXT,
    data_servico DATE
);
""")

conn.commit()
conn.close()
