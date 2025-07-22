from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response, render_template_string
from collections import defaultdict
from .forms import VehicleForm, ManutencaoForm
from .models import db, Veiculo, Manutencao
from alertas import gerar_resumo_veiculos, extrair_dados, disparar_alertas_reais
from datetime import datetime, date
from xhtml2pdf import pisa
from io import BytesIO
from flask_login import login_user, logout_user, login_required, current_user
from .models import Usuario
from functools import wraps
from flask import abort
from app.models import LogSistema
from app.models import registrar_log, get_ip_real
from flask import session
from app.permissoes import tem_permissao
from zoneinfo import ZoneInfo
from .utils import detectar_alteracoes
from flask_wtf import CSRFProtect
from flask import jsonify
from app.forms import PneuAplicadoForm
from app.models import PneuAplicado
from flask import send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from app.forms import EstoquePneuForm
from app.models import EstoquePneu


main = Blueprint('main', __name__)

def requer_tipo(*tipos_autorizados):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated and current_user.tipo in tipos_autorizados:
                return f(*args, **kwargs)
            else:
                flash("Acesso não autorizado para este usuário.", "danger")
                return redirect(url_for('main.index'))
        return wrapper
    return decorator




@main.route('/')
@login_required
def index():
    print(f"Usuário autenticado? {current_user.is_authenticated}")
    hoje = date.today()
    todos = Veiculo.query.order_by(Veiculo.placa).all()

    veiculos = [
        v for v in todos if (
            (v.km_para_preventiva and v.km_para_preventiva <= 5000) or
            (v.km_para_intermediaria and v.km_para_intermediaria <= 5000) or
            (v.km_para_diferencial and v.km_para_diferencial <= 5000) or
            (v.km_para_cambio and v.km_para_cambio <= 5000) or
            (v.data_proxima_calibragem and v.data_proxima_calibragem <= hoje)
        )
    ]

    return render_template('index.html', veiculos=veiculos, current_date=hoje)


@main.route('/atualizar-km/<int:id>', methods=['POST'])
@login_required
@requer_tipo("master", "comum")
def atualizar_km(id):
    veiculo = Veiculo.query.get_or_404(id)
    novo_km = request.form.get('km_atual')
    if novo_km and novo_km.isdigit():
        veiculo.km_atual = int(novo_km)
        db.session.commit()
        registrar_log(current_user, f"Atualizou o KM do veículo {veiculo.placa} para {novo_km}")
        flash(f'KM do veículo {veiculo.placa} atualizado para {novo_km}', 'success')
    else:
        flash('KM inválido. Digite um número válido.', 'warning')
    return redirect(url_for('main.lista_placas'))

@main.route('/cadastro-veiculo', methods=['GET', 'POST'])
@login_required
@requer_tipo("master", "comum", "teste", "visualizador")  # permite acesso à página para leitura
def cadastro_veiculo():
    veiculo_id = request.args.get('id')
    form = VehicleForm()

    # Edição: carregando veículo existente
    if veiculo_id:
        veiculo = Veiculo.query.get_or_404(veiculo_id)

        if request.method == 'GET':
            # Preenche os campos do formulário para exibição
            form.placa.data = veiculo.placa
            form.modelo.data = veiculo.modelo
            form.fabricante.data = veiculo.fabricante
            form.ano.data = veiculo.ano
            form.unidade.data = veiculo.unidade
            form.motorista.data = veiculo.motorista
            form.km_ultima_revisao_preventiva.data = veiculo.km_ultima_revisao_preventiva
            form.km_ultima_revisao_intermediaria.data = veiculo.km_ultima_revisao_intermediaria
            form.km_troca_preventiva.data = veiculo.km_troca_preventiva
            form.km_troca_intermediaria.data = veiculo.km_troca_intermediaria
            form.km_atual.data = veiculo.km_atual
            form.troca_oleo_diferencial.data = veiculo.troca_oleo_diferencial
            form.intervalo_oleo_diferencial.data = veiculo.intervalo_oleo_diferencial
            form.troca_oleo_cambio.data = veiculo.troca_oleo_cambio
            form.intervalo_oleo_cambio.data = veiculo.intervalo_oleo_cambio
            form.placa_1.data = veiculo.placa_1
            form.placa_2.data = veiculo.placa_2
            form.data_calibragem.data = veiculo.data_calibragem

        elif form.validate_on_submit():
            if not tem_permissao(current_user.tipo, "alterar_dados"):
                flash("Você não tem permissão para alterar veículos.", "danger")
                return redirect(url_for('main.cadastro_veiculo', id=veiculo.id))

            # Atualiza os dados do veículo
            veiculo.placa = form.placa.data.upper()
            veiculo.modelo = form.modelo.data.upper()
            veiculo.fabricante = form.fabricante.data.upper()
            veiculo.ano = form.ano.data.upper()
            veiculo.unidade = form.unidade.data.upper()
            veiculo.motorista = form.motorista.data.upper()
            veiculo.km_ultima_revisao_preventiva = form.km_ultima_revisao_preventiva.data
            veiculo.km_ultima_revisao_intermediaria = form.km_ultima_revisao_intermediaria.data
            veiculo.km_troca_preventiva = form.km_troca_preventiva.data
            veiculo.km_troca_intermediaria = form.km_troca_intermediaria.data
            veiculo.km_atual = form.km_atual.data
            veiculo.troca_oleo_diferencial = form.troca_oleo_diferencial.data
            veiculo.intervalo_oleo_diferencial = form.intervalo_oleo_diferencial.data
            veiculo.troca_oleo_cambio = form.troca_oleo_cambio.data
            veiculo.intervalo_oleo_cambio = form.intervalo_oleo_cambio.data
            veiculo.placa_1 = form.placa_1.data.upper() if form.placa_1.data else None
            veiculo.placa_2 = form.placa_2.data.upper() if form.placa_2.data else None
            veiculo.data_calibragem = form.data_calibragem.data

            db.session.commit()
            registrar_log(current_user, f"Atualizou o veículo {veiculo.placa}")
            flash(f'Veículo {veiculo.placa} atualizado com sucesso!', 'success')
            return redirect(url_for('main.cadastro_veiculo', id=veiculo.id))

    else:
        # Cadastro novo
        if form.validate_on_submit():
            if not tem_permissao(current_user.tipo, "alterar_dados"):
                flash("Você não tem permissão para cadastrar novos veículos.", "danger")
                return redirect(url_for('main.cadastro_veiculo'))

            placa_formatada = form.placa.data.upper()
            existente = Veiculo.query.filter_by(placa=placa_formatada).first()
            if existente:
                flash(f"A placa {placa_formatada} já está cadastrada.", "warning")
                return redirect(url_for('main.cadastro_veiculo'))

            veiculo = Veiculo(
                placa=placa_formatada,
                modelo=form.modelo.data.upper(),
                fabricante=form.fabricante.data.upper(),
                ano=form.ano.data.upper(),
                unidade=form.unidade.data.upper(),
                motorista=form.motorista.data.upper(),
                km_ultima_revisao_preventiva=form.km_ultima_revisao_preventiva.data,
                km_ultima_revisao_intermediaria=form.km_ultima_revisao_intermediaria.data,
                km_troca_preventiva=form.km_troca_preventiva.data,
                km_troca_intermediaria=form.km_troca_intermediaria.data,
                km_atual=form.km_atual.data or 0,
                troca_oleo_diferencial=form.troca_oleo_diferencial.data,
                intervalo_oleo_diferencial=form.intervalo_oleo_diferencial.data,
                troca_oleo_cambio=form.troca_oleo_cambio.data,
                intervalo_oleo_cambio=form.intervalo_oleo_cambio.data,
                placa_1=form.placa_1.data.upper() if form.placa_1.data else None,
                placa_2=form.placa_2.data.upper() if form.placa_2.data else None,
                data_calibragem=form.data_calibragem.data
            )

            db.session.add(veiculo)
            db.session.commit()
            registrar_log(current_user, f"Cadastrou o veículo {veiculo.placa}")
            flash(f'Veículo {veiculo.placa} cadastrado com sucesso!', 'success')
            return redirect(url_for('main.cadastro_veiculo', id=veiculo.id))

    return render_template('vehicle_register.html', form=form)

@main.route('/editar-veiculo/<int:id>', methods=['GET', 'POST'])
@login_required
@requer_tipo("master")
def editar_veiculo(id):
    veiculo = Veiculo.query.get_or_404(id)

    novos_dados = {
        "placa": request.form.get('placa', '').upper(),
        "carreta1": request.form.get('carreta1', '').upper(),
        "carreta2": request.form.get('carreta2', '').upper(),
        "motorista": request.form.get('motorista', '').upper(),
        "modelo": request.form.get('modelo', '').upper(),
        "fabricante": request.form.get('fabricante', '').upper(),
        "ano": request.form.get('ano', '').upper(),
        "km_atual": int(request.form.get('km_atual')) if request.form.get('km_atual', '').isdigit() else 0
    }

    alteracoes = detectar_alteracoes(veiculo, novos_dados)
    print("Alterações detectadas:", alteracoes)


    if alteracoes:
        for campo, valor in novos_dados.items():
            setattr(veiculo, campo, valor)

        db.session.commit()
        registrar_log(current_user, f"Editou veículo {veiculo.placa}: " + "; ".join(alteracoes))
        flash(f'Dados do veículo {veiculo.placa} atualizados no painel!', 'success')
    else:
        flash(f'Nenhuma alteração detectada no veículo {veiculo.placa}.', 'info')

    return redirect(url_for('main.lista_placas'))



@main.route('/realizar-manutencao', methods=['GET', 'POST'])
@login_required
@requer_tipo("master", "comum", "teste", "visualizador")
def realizar_manutencao():
    form = ManutencaoForm()
    form.veiculo_id.choices = [(v.id, v.placa) for v in Veiculo.query.order_by(Veiculo.placa).all()]

    if form.validate_on_submit():
        # ❌ Impede submissão se o usuário não tiver permissão
        if not tem_permissao(current_user.tipo, "alterar_dados"):
            flash("Você não tem permissão para registrar manutenções.", "warning")
            return redirect(url_for('main.realizar_manutencao'))

        veiculo = Veiculo.query.get(form.veiculo_id.data)
        tipo = form.tipo.data.upper()
        km_realizado = form.km_realizado.data

        # Criação da manutenção
        manut = Manutencao(
            veiculo_id=veiculo.id,
            motorista=veiculo.motorista,
            placa=veiculo.placa,
            modelo=veiculo.modelo,
            fabricante=veiculo.fabricante,
            km_atual=km_realizado,
            km_troca=km_realizado,
            data_troca=form.data.data,
            data_proxima=None,
            observacoes=form.observacoes.data.upper() if form.observacoes.data else None
        )
        db.session.add(manut)

        # Atualiza o campo correto do veículo
        if tipo == 'PREVENTIVA':
            veiculo.km_ultima_revisao_preventiva = km_realizado
            veiculo.km_ultima_revisao_intermediaria = km_realizado
        elif tipo == 'INTERMEDIARIA':
            veiculo.km_ultima_revisao_intermediaria = km_realizado
        elif tipo == 'DIFERENCIAL':
            veiculo.troca_oleo_diferencial = km_realizado
        elif tipo == 'CAMBIO':
            veiculo.troca_oleo_cambio = km_realizado

        db.session.commit()
        registrar_log(current_user, f"Registrou manutenção {tipo} no veículo {veiculo.placa} na KM {km_realizado}")
        flash(f'{tipo.title()} registrada com sucesso para {veiculo.placa}!', 'success')
        return redirect(url_for('main.lista_placas'))

    return render_template('realizar_manutencao.html', form=form)


@main.route('/excluir-veiculo/<int:id>')
@login_required
@requer_tipo("master","teste")
def excluir_veiculo(id):
    veiculo = Veiculo.query.get_or_404(id)
    Manutencao.query.filter_by(veiculo_id=veiculo.id).delete()  # Apaga manutenções primeiro
    db.session.delete(veiculo)
    db.session.commit()
    registrar_log(current_user, f"Excluiu o veículo {veiculo} e suas manutenções vinculadas")
    flash(f'Veículo {veiculo.placa} removido com sucesso.', 'info')
    return redirect(url_for('main.lista_placas'))



@main.route('/placas')
@login_required
@requer_tipo("master", "comum","teste")
def lista_placas():
    veiculos = Veiculo.query.order_by(Veiculo.unidade, Veiculo.placa).all()
    unidades = defaultdict(list)
    for v in veiculos:
        unidades[v.unidade.upper()].append(v)

    return render_template('placas.html', unidades=unidades, current_date=date.today())



@main.route('/unidade/<unidade>')
@login_required
@requer_tipo("master", "comum")
def filtrar_unidade(unidade):
    veiculos = Veiculo.query.filter_by(unidade=unidade.upper()).order_by(Veiculo.placa).all()
    return render_template('index.html', veiculos=veiculos, current_date=date.today())


@main.route('/nova-manutencao')
@login_required
@requer_tipo("master", "comum")
def nova_manutencao():
    return render_template('new_entry.html')


#@main.route('/teste-alerta')
#def teste_alerta():
 #   from alertas import disparar_alertas_reais
  #  disparar_alertas_reais()
  #  flash("🚨 Alerta via template disparado com sucesso!", "success")
  #  return redirect(url_for('main.index'))

@main.route('/teste-alerta')
@login_required
def teste_alerta():
    if current_user.tipo.upper() != 'MASTER':
        flash("❌ Apenas usuários MASTER podem disparar alertas!", "danger")
        return redirect(url_for('main.index'))

    from alertas import disparar_alertas_multiplos
    disparar_alertas_multiplos()
    flash("🚨 Alertas enviados com sucesso!", "success")
    return redirect(url_for('main.index'))



@main.route('/gerar-relatorio-pdf')
@login_required
@requer_tipo("master", "comum")
def gerar_relatorio_pdf():
    linhas = extrair_dados()

    if not linhas:
        flash("Nenhum veículo está com revisão próxima.", "info")
        return redirect(url_for('main.index'))

    html = render_template_string("""
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>

        <style>
            body {
                font-family: Helvetica, Arial, sans-serif;
                padding: 30px;
                color: #333;
            }
            h1 {
                text-align: center;
                color: #004085;
                border-bottom: 2px solid #007bff;
                padding-bottom: 5px;
                margin-bottom: 30px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }
            th, td {
                border: 1px solid #999;
                padding: 8px;
                font-size: 12px;
                text-align: center;
            }
            th {
                background-color: #e3e3e3;
            }
            .footer {
                margin-top: 40px;
                font-size: 11px;
                text-align: center;
                color: #777;
            }
        </style>
    </head>
    <body>
        <h1>Relatório de Manutenção</h1>
        <p><strong>Data:</strong> {{ hoje }}</p>
        <table>
            <thead>
                <tr>
                    <th>Placa</th>
                    <th>Motorista</th>
                    <th>KM Atual</th>
                    <th>Preventiva</th>
                    <th>Intermediária</th>
                </tr>
            </thead>
            <tbody>
                {% for linha in linhas %}
                <tr>
                    <td>{{ linha.placa }}</td>
                    <td>{{ linha.motorista }}</td>
                    <td>{{ linha.km_atual }}</td>
                    <td>{{ linha.preventiva }}</td>
                    <td>{{ linha.intermediaria }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <div class="footer">
            Sistema de Gestão de Frota - {{ hoje }}
        </div>
    </body>
    </html>
    """, hoje=datetime.today().strftime('%d/%m/%Y'), linhas=linhas)

    pdf_buffer = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=pdf_buffer)

    response = make_response(pdf_buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=relatorio_manutencao.pdf'  # 🔽 Gatilho pra download
    return response

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome_usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        usuario = Usuario.query.filter_by(usuario=nome_usuario).first()
        if usuario and usuario.verificar_senha(senha):
            login_user(usuario)
            session.permanent = True  # ⏱️ ativa limite de tempo de sessão
            registrar_log(usuario, f"Fez login no sistema")
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')
    return render_template('login.html', ano=datetime.now().year)



@main.route('/logout')
@login_required
def logout():
    registrar_log(current_user, f"Fez logout do sistema")
    logout_user()
    flash("Logout realizado com sucesso!", "info")
    return redirect(url_for('main.login'))


@main.route('/usuarios', methods=['GET'])
@login_required
@requer_tipo('master')
def gerenciar_usuarios():
    usuarios = Usuario.query.order_by(Usuario.id).all()
    return render_template('cadastro_usuario.html', usuarios=usuarios)

@main.route('/usuarios/adicionar', methods=['POST'])
@login_required
@requer_tipo('master')
def adicionar_usuario():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    tipo = request.form.get('tipo').lower()

    if Usuario.query.filter_by(usuario=nome).first():
        flash('Usuário já existe!', 'warning')
    else:
        novo = Usuario(usuario=nome.lower(), nome=nome.title(), tipo=tipo)
        novo.set_senha(senha)
        db.session.add(novo)
        db.session.commit()
        registrar_log(current_user, f"Cadastrou o usuário {nome}")
        flash(f'Usuário {nome} criado com sucesso!', 'success')

    return redirect(url_for('main.gerenciar_usuarios'))


@main.route('/usuarios/remover/<int:id>', methods=['POST'])
@login_required
@requer_tipo('master')
def remover_usuario(id):
    usuario = Usuario.query.get_or_404(id)

    if usuario.usuario == 'admin':
        flash('Esse usuário não pode ser removido.', 'danger')
    else:
        db.session.delete(usuario)
        db.session.commit()
        registrar_log(current_user, f"Removeu o usuário {usuario.nome}")
        flash(f'Usuário {usuario.nome} removido com sucesso.', 'info')

    return redirect(url_for('main.gerenciar_usuarios'))


from zoneinfo import ZoneInfo

@main.route("/logs")
@login_required
def exibir_logs():
    logs = LogSistema.query.order_by(LogSistema.data.desc()).limit(200).all()

    for log in logs:
        if log.data.tzinfo is None:
            log.data = log.data.replace(tzinfo=ZoneInfo("UTC"))
        log.data = log.data.astimezone(ZoneInfo("America/Fortaleza"))

    # 🔥 Ordena no Python após aplicar timezone
    logs.sort(key=lambda l: l.data, reverse=True)

    return render_template("logs.html", logs=logs)

@main.route('/manutencao/<placa>', methods=['POST'])
@login_required
def atualizar_manutencao(placa):
    if current_user.tipo.upper() != 'MASTER':
        abort(403)

    veiculo = Veiculo.query.filter_by(placa=placa).first_or_404()
    veiculo.em_manutencao = not veiculo.em_manutencao
    db.session.commit()
    return jsonify({'status': 'ok', 'ativo': veiculo.em_manutencao})


@main.route('/pneus', methods=['GET', 'POST'])
@login_required
def mostrar_pneus():
    form = PneuAplicadoForm()

    if form.validate_on_submit():
        numero_fogo = form.numero_fogo.data.upper()
        pneu_estoque = EstoquePneu.query.filter_by(numero_fogo=numero_fogo, status='DISPONIVEL').first()
        if not pneu_estoque:
            registrar_log(current_user, f"Tentativa de aplicar pneu indisponível: {numero_fogo}")
            flash('❌ Este pneu não está disponível no estoque!', 'danger')
            return render_template('pneus.html', form=form, pneus=[])

        pneu = PneuAplicado(
            placa=form.placa.data.upper(),
            referencia=form.referencia.data.upper(),
            dot=form.dot.data.upper(),
            numero_fogo=numero_fogo,
            quantidade=form.quantidade.data,
            data_aplicacao=form.data_aplicacao.data,
            unidade=form.unidade.data,
            observacoes=form.observacoes.data,
            extra=form.extra.data
        )
        db.session.add(pneu)
        pneu_estoque.status = 'APLICADO'
        db.session.commit()

        registrar_log(current_user, f"Pneu aplicado: {numero_fogo} na placa {form.placa.data.upper()}")
        flash('✅ Pneu aplicado com sucesso!', 'success')
        return redirect('/pneus')

    placa = request.args.get('placa', '').upper()
    fogo = request.args.get('numero_fogo', '').upper()
    unidade = request.args.get('unidade', '')
    query = PneuAplicado.query
    if placa:
        query = query.filter(PneuAplicado.placa.ilike(f"%{placa}%"))
    if fogo:
        query = query.filter(PneuAplicado.numero_fogo.ilike(f"%{fogo}%"))
    if unidade:
        query = query.filter(PneuAplicado.unidade == unidade)

    pneus = query.order_by(PneuAplicado.id.desc()).limit(15).all()
    return render_template('pneus.html', form=form, pneus=pneus)


@main.route('/pneus/editar_placa', methods=['POST'])
@login_required
def editar_placa():
    id = request.form.get('id')
    nova_placa = request.form.get('placa', '').upper()
    nova_unidade = request.form.get('unidade', '').upper()

    pneu = PneuAplicado.query.get(id)
    if pneu:
        pneu.placa = nova_placa
        pneu.unidade = nova_unidade
        db.session.commit()
        registrar_log(current_user, f"Edição de placa do pneu ID {id}: nova placa {nova_placa}, unidade {nova_unidade}")
        flash(f'✅ Dados atualizados com sucesso!', 'success')
    else:
        registrar_log(current_user, f"Tentativa de editar placa: pneu ID {id} não encontrado")
        flash('❌ Pneu não encontrado', 'danger')

    return redirect('/pneus')


@main.route('/pneus/pdf', methods=['GET'])
@login_required
def gerar_pdf():
    placa = request.args.get('placa', '').upper()
    fogo = request.args.get('numero_fogo', '').upper()
    unidade = request.args.get('unidade', '')

    query = PneuAplicado.query
    if placa:
        query = query.filter(PneuAplicado.placa.ilike(f"%{placa}%"))
    if fogo:
        query = query.filter(PneuAplicado.numero_fogo.ilike(f"%{fogo}%"))
    if unidade:
        query = query.filter(PneuAplicado.unidade == unidade)

    pneus = query.order_by(PneuAplicado.id.desc()).all()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, height - 50, "Relatório de Pneus Aplicados")

    pdf.setFont("Helvetica", 10)
    y = height - 80
    for i, p in enumerate(pneus, start=1):
        linha = f"{i}. Placa: {p.placa} | Ref: {p.referencia} | DOT: {p.dot} | Fogo: {p.numero_fogo} | Qtd: {p.quantidade} | Data: {p.data_aplicacao.strftime('%d/%m/%Y')} | Unidade: {p.unidade}"
        pdf.drawString(50, y, linha)
        y -= 15
        if y < 50:
            pdf.showPage()
            y = height - 50

    pdf.save()
    buffer.seek(0)
    registrar_log(current_user, f"PDF de pneus aplicado gerado: placa={placa}, fogo={fogo}, unidade={unidade}")
    return send_file(buffer, as_attachment=True, download_name="pneus_aplicados.pdf", mimetype='application/pdf')

@main.route('/estoque', methods=['GET', 'POST'])
@login_required
def cadastrar_estoque():
    form = EstoquePneuForm()

    if form.validate_on_submit():
        existente = EstoquePneu.query.filter_by(numero_fogo=form.numero_fogo.data.upper()).first()
        if existente:
            registrar_log(current_user, f"Tentativa duplicada de cadastro: {form.numero_fogo.data.upper()}")
            flash('❌ Este número de fogo já está cadastrado no estoque.', 'danger')
            return redirect('/estoque')

        pneu = EstoquePneu(
            numero_fogo=form.numero_fogo.data.upper(),
            vida=form.vida.data,
            modelo=form.modelo.data.upper(),
            desenho=form.desenho.data.upper(),
            dot=form.dot.data.upper(),
            data_entrada=form.data_entrada.data,
            observacoes=form.observacoes.data
        )
        db.session.add(pneu)
        db.session.commit()
        registrar_log(current_user, f"Cadastro de pneu no estoque: {form.numero_fogo.data.upper()}")
        flash('✅ Pneu cadastrado no estoque com sucesso!', 'success')
        return redirect('/estoque')

    return render_template('estoque_pneus.html', form=form)


@main.route('/estoque/visualizar', methods=['GET'])
@login_required
def visualizar_estoque():
    numero_fogo = request.args.get('numero_fogo', '').upper()
    modelo = request.args.get('modelo', '').upper()
    desenho = request.args.get('desenho', '').upper()

    query = EstoquePneu.query.filter_by(status='DISPONIVEL')
    if numero_fogo:
        query = query.filter(EstoquePneu.numero_fogo.ilike(f"%{numero_fogo}%"))
    if modelo:
        query = query.filter(EstoquePneu.modelo.ilike(f"%{modelo}%"))
    if desenho:
        query = query.filter(EstoquePneu.desenho == desenho)

    pneus = query.order_by(EstoquePneu.id.desc()).all()
    total_estoque = EstoquePneu.query.filter_by(status='DISPONIVEL').count()
    total_aplicados = PneuAplicado.query.count()
    liso = EstoquePneu.query.filter_by(desenho='LISO', status='DISPONIVEL').count()
    borrachudo = EstoquePneu.query.filter_by(desenho='BORRACHUDO', status='DISPONIVEL').count()

    registrar_log(current_user, f"Visualização do estoque: fogo={numero_fogo}, modelo={modelo}, desenho={desenho}")
    return render_template('estoque_visualizar.html', pneus=pneus,
                           total_estoque=total_estoque,
                           total_aplicados=total_aplicados,
                           liso=liso, borrachudo=borrachudo)



@main.route('/estoque/pdf', methods=['GET'])
@login_required
def gerar_pdf_estoque():
    numero_fogo = request.args.get('numero_fogo', '').upper()
    modelo = request.args.get('modelo', '').upper()
    desenho = request.args.get('desenho', '').upper()

    query = EstoquePneu.query
    if numero_fogo:
        query = query.filter(EstoquePneu.numero_fogo.ilike(f"%{numero_fogo}%"))
    if modelo:
        query = query.filter(EstoquePneu.modelo.ilike(f"%{modelo}%"))
    if desenho:
        query = query.filter(EstoquePneu.desenho == desenho)

    pneus = query.order_by(EstoquePneu.id.desc()).all()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, height - 50, "📦 Relatório de Estoque de Pneus")

    pdf.setFont("Helvetica", 10)
    y = height - 80
    for i, p in enumerate(pneus, start=1):
        linha = f"{i}. Fogo: {p.numero_fogo} | Vida: {p.vida} | Modelo: {p.modelo} | Desenho: {p.desenho} | DOT: {p.dot} | Entrada: {p.data_entrada.strftime('%d/%m/%Y')}"
        pdf.drawString(50, y, linha)
        y -= 15
        if y < 50:
            pdf.showPage()
            y = height - 50

    pdf.save()
    buffer.seek(0)

    # 📝 Registrar log da ação
    registrar_log(current_user, f"PDF do estoque gerado: fogo={numero_fogo}, modelo={modelo}, desenho={desenho}")

    return send_file(buffer, as_attachment=True, download_name="estoque_pneus.pdf", mimetype='application/pdf')


@main.route('/pneus/detalhes', methods=['GET'])
@login_required
def detalhes_pneu():
    numero_fogo = request.args.get('numero_fogo', '').upper()

    # Verifica se já foi aplicado
    pneu = PneuAplicado.query.filter_by(numero_fogo=numero_fogo).order_by(PneuAplicado.id.desc()).first()
    if pneu:
        return jsonify({
            'placa': pneu.placa,
            'referencia': pneu.referencia,   # campo existe no PneuAplicado
            'dot': pneu.dot,
            'quantidade': 1
        })

    # Verifica no estoque
    estoque = EstoquePneu.query.filter_by(numero_fogo=numero_fogo, status='DISPONIVEL').first()
    if estoque:
        return jsonify({
            'placa': '',                      # Ainda não aplicado
            'referencia': estoque.modelo,     # usa 'modelo' como referência
            'dot': estoque.dot,
            'quantidade': 1
        })

    return jsonify({})
