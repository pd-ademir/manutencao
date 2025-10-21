from .extensions import db
from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from zoneinfo import ZoneInfo
from flask_sqlalchemy import SQLAlchemy




class Manutencao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'), nullable=False)

    tipo = db.Column(db.String(50), nullable=False)  # ← Novo campo
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
    placa_1 = db.Column(db.String(10))
    placa_2 = db.Column(db.String(10))    
    data_calibragem = db.Column(db.Date)    
    troca_oleo_diferencial = db.Column(db.Integer)
    intervalo_oleo_diferencial = db.Column(db.Integer)    
    troca_oleo_cambio = db.Column(db.Integer)
    intervalo_oleo_cambio = db.Column(db.Integer)    
    km_ultima_revisao_preventiva = db.Column(db.Integer)
    km_ultima_revisao_intermediaria = db.Column(db.Integer)
    km_troca_preventiva = db.Column(db.Integer, nullable=False)
    km_troca_intermediaria = db.Column(db.Integer, nullable=False)
    km_atual = db.Column(db.Integer, default=0)
    data_ultima_atualizacao_km = db.Column(db.DateTime)
    data_ultima_revisao_preventiva = db.Column(db.Date)
    data_ultima_revisao_intermediaria = db.Column(db.Date)
    data_troca_oleo_diferencial = db.Column(db.Date)
    data_troca_oleo_cambio = db.Column(db.Date)
    data_proxima_calibragem = db.Column(db.Date, nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    em_manutencao = db.Column(db.Boolean, default=False)
    manutencoes = db.relationship('Manutencao', backref='veiculo', lazy=True)
    data_proxima_revisao_carreta = db.Column(db.Date)

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



class LogSistema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    acao = db.Column(db.String(200), nullable=False)
    ip = db.Column(db.String(50), nullable=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    usuario = db.relationship('Usuario', backref='logs')



def get_ip_real():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr or "IP desconhecido"


def registrar_log(usuario, acao):
    print("Registrando log:", acao)
    ip = get_ip_real()
    data = datetime.now(ZoneInfo("America/Fortaleza"))

    log = LogSistema(
        usuario_id=usuario.id,
        acao=acao,
        ip=ip,
        data=data
    )
    db.session.add(log)
    db.session.commit()





# Apenas para testes iniciais — depois montamos o CRUD certo
whatsapp_numeros = [
      # <- insira aqui seu número de teste
    '18981430410'
]


from app.extensions import db

class PneuAplicado(db.Model):
    __bind_key__ = 'pneus'
    __tablename__ = 'pneus_aplicados'

    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(10), nullable=False)
    referencia = db.Column(db.String(50), nullable=False)
    dot = db.Column(db.String(10), nullable=False)
    numero_fogo = db.Column(db.String(20), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_aplicacao = db.Column(db.Date, nullable=False)
    unidade = db.Column(db.String(30), nullable=False)
    observacoes = db.Column(db.Text, nullable=True)
    extra = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<PneuAplicado {self.placa} - {self.referencia}>'

class EstoquePneu(db.Model):
    __bind_key__ = 'pneus'
    __tablename__ = 'estoque_pneus'

    id = db.Column(db.Integer, primary_key=True)
    numero_fogo = db.Column(db.String(20), unique=True, nullable=False)
    vida = db.Column(db.Integer, nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    desenho = db.Column(db.String(20), nullable=False)
    dot = db.Column(db.String(10), nullable=True)
    data_entrada = db.Column(db.Date, nullable=False)
    observacoes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='DISPONIVEL')  # ou 'APLICADO'


    def __repr__(self):
        return f"<EstoquePneu {self.numero_fogo}>"



# relatório de bloqueios e liberações de veículos

class HistoricoBloqueio(db.Model):
    __tablename__ = 'historico_bloqueio'
    
    id = db.Column(db.Integer, primary_key=True)
    # CORREÇÃO: de 'veiculos.id' para 'veiculo.id'
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'), nullable=False)
    
    # Detalhes do bloqueio
    tipo_manutencao = db.Column(db.String(100), nullable=False)
    data_bloqueio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    km_bloqueio = db.Column(db.Integer, nullable=False)
    
    # Detalhes da liberação
    liberado = db.Column(db.Boolean, default=False)
    data_liberacao = db.Column(db.DateTime, nullable=True)
    # CORREÇÃO: de 'manutencoes.id' para 'manutencao.id'
    manutencao_id = db.Column(db.Integer, db.ForeignKey('manutencao.id'), nullable=True) # Link para a manutenção que liberou

    veiculo = db.relationship('Veiculo', backref=db.backref('historico_bloqueios', lazy=True))

    def __repr__(self):
        status = "Liberado" if self.liberado else "Pendente"
        return f'<Bloqueio {self.id} - Veículo {self.veiculo.placa} ({status})>'
