from app import create_app
from flask_login import LoginManager
from datetime import timedelta


app = create_app()
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

if __name__ == '__main__':
    app.run(debug=True)
    # Adicionado host='0.0.0.0' para aceitar conexões da sua rede local
   # app.run(debug=True, host='0.0.0.0')




