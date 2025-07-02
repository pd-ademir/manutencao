from .extensions import db
from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request


class Manutencao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'), nullable=False)

    motorista = db.Column(db.String(100), nullable=False)
    placa = db.Column(db.String(10), nullable=False)
    modelo = db.Column(db.String(50))
    fabricante = db.Column(db.String(50))
    km_atual = db.Column(db.Integer)
    km_troca = db.Column(db.Integer)
    data_troca = db.Column(db.Date)
    data_proxima = db.Column(db.Date)
    observacoes = db.Column(db.Text)

    def __repr__(self):
        return f'<Manutencao {self.placa} - {self.data_troca}>'


class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(10), nullable=False, unique=True)
    modelo = db.Column(db.String(50), nullable=False)
    fabricante = db.Column(db.String(50))
    ano = db.Column(db.String(4))
    unidade = db.Column(db.String(50), nullable=False)
    motorista = db.Column(db.String(100), nullable=False)

    # Placas adicionais
    placa_1 = db.Column(db.String(10))
    placa_2 = db.Column(db.String(10))

    # Calibragem
    data_calibragem = db.Column(db.Date)

    # Troca de óleo — diferencial
    troca_oleo_diferencial = db.Column(db.Integer)            # KM da última troca
    intervalo_oleo_diferencial = db.Column(db.Integer)        # Intervalo configurado até a próxima

    # Troca de óleo — câmbio
    troca_oleo_cambio = db.Column(db.Integer)
    intervalo_oleo_cambio = db.Column(db.Integer)

    # Revisões
    km_ultima_revisao_preventiva = db.Column(db.Integer)
    km_ultima_revisao_intermediaria = db.Column(db.Integer)
    km_troca_preventiva = db.Column(db.Integer, nullable=False)
    km_troca_intermediaria = db.Column(db.Integer, nullable=False)

    km_atual = db.Column(db.Integer, default=0)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento com manutenções realizadas
    manutencoes = db.relationship('Manutencao', backref='veiculo', lazy=True)

    # --- Propriedades calculadas ---

    @property
    def km_para_preventiva(self):
        if all(isinstance(v, int) for v in [self.km_ultima_revisao_preventiva, self.km_troca_preventiva, self.km_atual]):
            return (self.km_ultima_revisao_preventiva + self.km_troca_preventiva) - self.km_atual
        return None

    @property
    def km_para_intermediaria(self):
        if all(isinstance(v, int) for v in [self.km_ultima_revisao_intermediaria, self.km_troca_intermediaria, self.km_atual]):
            return (self.km_ultima_revisao_intermediaria + self.km_troca_intermediaria) - self.km_atual
        return None

    @property
    def km_para_diferencial(self):
        if all(isinstance(v, int) for v in [self.troca_oleo_diferencial, self.intervalo_oleo_diferencial, self.km_atual]):
            return (self.troca_oleo_diferencial + self.intervalo_oleo_diferencial) - self.km_atual
        return None

    @property
    def km_para_cambio(self):
        if all(isinstance(v, int) for v in [self.troca_oleo_cambio, self.intervalo_oleo_cambio, self.km_atual]):
            return (self.troca_oleo_cambio + self.intervalo_oleo_cambio) - self.km_atual
        return None

    @property
    def data_proxima_calibragem(self):
        if self.data_calibragem:
            return self.data_calibragem + timedelta(days=20)
        return None

    def __repr__(self):
        return f'<Veiculo {self.placa}>'
    


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)  # 👈 nome de usuário (login)
    nome = db.Column(db.String(50), nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

from datetime import datetime

class LogSistema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    acao = db.Column(db.String(200), nullable=False)
    ip = db.Column(db.String(50), nullable=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    usuario = db.relationship('Usuario', backref='logs')


def registrar_log(usuario, acao):
    from app.extensions import db
    from app.models import LogSistema

    ip = request.remote_addr or "IP desconhecido"
    log = LogSistema(usuario_id=usuario.id, acao=acao, ip=ip)
    db.session.add(log)
    db.session.commit()



    
# Apenas para testes iniciais — depois montamos o CRUD certo
whatsapp_numeros = [
      # <- insira aqui seu número de teste
    '18981430410'
]

