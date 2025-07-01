from app import create_app
from app.models import db

app = create_app()

with app.app_context():
    with db.engine.connect() as connection:
        connection.execute(db.text("ALTER TABLE veiculo ADD COLUMN km_ultima_revisao INTEGER"))
        print("🚀 Campo km_ultima_revisao adicionado com sucesso!")
