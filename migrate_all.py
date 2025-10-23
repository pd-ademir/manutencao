import sqlite3
from sqlalchemy import create_engine, text, inspect

# Configurações dos bancos
databases = {
    'checklist': {
        'sqlite_path': 'instance/checklist.sqlite3',
        'mysql_url': 'mysql+pymysql://ornilio:%40Machado2025@136.113.79.172/checklist'
    },
    'pneus': {
        'sqlite_path': 'instance/pneus.sqlite3',
        'mysql_url': 'mysql+pymysql://ornilio:%40Machado2025@136.113.79.172/pneus'
    },
    'manutencao': {
        'sqlite_path': 'instance/db.sqlite3',
        'mysql_url': 'mysql+pymysql://ornilio:%40Machado2025@136.113.79.172/manutencao'
    }
}

def migrate_sqlite_to_mysql(sqlite_path, mysql_url):
    print(f"Iniciando migração de {sqlite_path} para {mysql_url}")
    
    # Conecta SQLite
    sqlite_conn = sqlite3.connect(sqlite_path)
    sqlite_cursor = sqlite_conn.cursor()
    
    # Cria engine MySQL
    engine = create_engine(mysql_url)
    inspector = inspect(engine)

    # Lista tabelas do SQLite
    sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in sqlite_cursor.fetchall()]
    
    with engine.connect() as conn:
        for table in tables:
            # Verifica se tabela existe no MySQL
            if not inspector.has_table(table):
                print(f"AVISO: A tabela '{table}' não existe no MySQL. Pule ou crie antes da migração.")
                continue
            
            # Busca dados do SQLite
            sqlite_cursor.execute(f"SELECT * FROM {table}")
            rows = sqlite_cursor.fetchall()
            if not rows:
                print(f"Tabela '{table}' vazia, pulando...")
                continue
            
            # Colunas para insert
            columns = [description[0] for description in sqlite_cursor.description]
            columns_str = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(columns))
            
            print(f"Migrando {len(rows)} registros da tabela '{table}'...")
            
            # Inserir dados no MySQL
            for row in rows:
                conn.execute(text(f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"), row)
    
    sqlite_conn.close()
    print(f"Migração do arquivo {sqlite_path} concluída.\n")

if __name__ == "__main__":
    for db_name, config in databases.items():
        migrate_sqlite_to_mysql(config['sqlite_path'], config['mysql_url'])
