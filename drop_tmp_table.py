from app import create_app, db

app = create_app()

with app.app_context():
    with db.engine.connect() as conn:
        conn.execute(db.text("DROP TABLE IF EXISTS _alembic_tmp_manutencao"))
        print("✅ Tabela temporária _alembic_tmp_manutencao removida com sucesso!")
