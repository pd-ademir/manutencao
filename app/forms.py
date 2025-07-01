from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, SelectField,
    DateField, TextAreaField, SubmitField
)
from wtforms.validators import DataRequired, Length, Optional
from datetime import datetime



class VehicleForm(FlaskForm):
    placa = StringField('Placa', validators=[DataRequired(), Length(min=7, max=10)])
    modelo = StringField('Modelo', validators=[DataRequired()])
    fabricante = StringField('Fabricante')
    ano = StringField('Ano', validators=[Length(min=4, max=4)])
    
    unidade = SelectField('Unidade', choices=[
        ('BAGAM', 'BAGAM'),
        ('BACRO', 'BACRO'),
        ('SPOT RN', 'SPOT RN'),
        ('SPOT PE', 'SPOT PE'),
        ('SMART', 'SMART')
    ], validators=[DataRequired()])
    
    motorista = StringField('Motorista', validators=[DataRequired()])
    placa_1 = StringField('Placa 1')
    placa_2 = StringField('Placa 2')
    data_calibragem = DateField('Data Calibragem', format='%Y-%m-%d', validators=[Optional()])
    
    troca_oleo_diferencial = IntegerField('Última Troca Diferencial (km)', validators=[Optional()])
    intervalo_oleo_diferencial = IntegerField('Intervalo Troca Diferencial (km)', validators=[Optional()])
    
    troca_oleo_cambio = IntegerField('Última Troca Câmbio (km)', validators=[Optional()])
    intervalo_oleo_cambio = IntegerField('Intervalo Troca Câmbio (km)', validators=[Optional()])
    
    km_ultima_revisao_preventiva = IntegerField('Última Revisão Preventiva')
    km_ultima_revisao_intermediaria = IntegerField('Última Revisão Intermediária')
    km_troca_preventiva = IntegerField('KM por Troca Preventiva', validators=[DataRequired()])
    km_troca_intermediaria = IntegerField('KM por Troca Intermediária', validators=[DataRequired()])
    
    km_atual = IntegerField('KM Atual')
    submit = SubmitField('Salvar')

class ManutencaoForm(FlaskForm):
    veiculo_id = SelectField('Placa', coerce=int, validators=[DataRequired()])
    data = DateField('Data da Manutenção', format='%Y-%m-%d', default=datetime.today)
    tipo = SelectField("Tipo de Manutenção", choices=[
    ("PREVENTIVA", "Preventiva"),
    ("INTERMEDIARIA", "Intermediária"),
    ("DIFERENCIAL", "Diferencial"),
    ("CAMBIO", "Câmbio")
    ], validators=[DataRequired()])
    km_realizado = IntegerField('KM Atual', validators=[DataRequired()])
    observacoes = TextAreaField('Observações')
    submit = SubmitField('Registrar')
