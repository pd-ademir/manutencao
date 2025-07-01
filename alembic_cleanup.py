from app import create_app, db

app = create_app()

with app.app_context():
    db.engine.execute("DROP TABLE IF EXISTS _alembic_tmp_manutencao;")
    print("🔥 Tabela _alembic_tmp_manutencao removida com sucesso!")
