from flask import Blueprint, render_template, request, redirect, flash, url_for
from app.checklist_form import ChecklistForm
from instance.checklist_db import engine_checklist
from sqlalchemy.sql import text
from collections import namedtuple


checklist_bp = Blueprint('checklist', __name__, template_folder='templates')

@checklist_bp.route('/novo', methods=['GET', 'POST'])
def novo_checklist():
    if request.method == 'POST':
        with engine_checklist.connect() as conn:
            for i in range(1, 101):
                placa = request.form.get(f"placa_{i}")
                item = request.form.get(f"item_{i}")
                if placa and item:
                    dados = {
                        "mes": request.form.get(f"mes_{i}"),
                        "data_registro": request.form.get(f"data_registro_{i}"),
                        "placa": placa,
                        "item": item,
                        "fonte": request.form.get(f"fonte_{i}"),
                        "tipo_manutencao": request.form.get(f"tipo_manutencao_{i}"),
                        "status": request.form.get(f"status_{i}"),
                        "ordem_servico": request.form.get(f"ordem_servico_{i}"),
                        "conclusao": request.form.get(f"conclusao_{i}"),
                        "data_servico": request.form.get(f"data_servico_{i}")
                    }

                    id_existente = request.form.get(f"id_{i}")
                    if id_existente:
                        update = text("""
                            UPDATE checklist SET
                                mes = :mes,
                                data_registro = :data_registro,
                                placa = :placa,
                                item = :item,
                                fonte = :fonte,
                                tipo_manutencao = :tipo_manutencao,
                                status = :status,
                                ordem_servico = :ordem_servico,
                                conclusao = :conclusao,
                                data_servico = :data_servico
                            WHERE id = :id
                        """)
                        dados["id"] = id_existente
                        conn.execute(update, dados)
                    else:
                        insert = text("""
                            INSERT INTO checklist (
                                mes, data_registro, placa, item,
                                fonte, tipo_manutencao, status,
                                ordem_servico, conclusao, data_servico
                            ) VALUES (
                                :mes, :data_registro, :placa, :item,
                                :fonte, :tipo_manutencao, :status,
                                :ordem_servico, :conclusao, :data_servico
                            )
                        """)
                        conn.execute(insert, dados)
            conn.commit()
        flash("Dados salvos com sucesso!", "success")
        return redirect(url_for('checklist.novo_checklist'))

    with engine_checklist.connect() as conn:
        registros = conn.execute(text("SELECT * FROM checklist ORDER BY id")).fetchall()

    linhas = []
    for i in range(100):
        if i < len(registros):
            r = registros[i]
            linhas.append({
                "id": r.id,
                "mes": r.mes or "",
                "data_registro": r.data_registro or "",
                "placa": r.placa or "",
                "item": r.item or "",
                "fonte": r.fonte or "",
                "tipo_manutencao": r.tipo_manutencao or "",
                "status": r.status or "",
                "ordem_servico": r.ordem_servico or "",
                "conclusao": r.conclusao or "",
                "data_servico": r.data_servico or ""
            })
        else:
            linhas.append({
                "id": "",
                "mes": "", "data_registro": "", "placa": "", "item": "",
                "fonte": "", "tipo_manutencao": "", "status": "",
                "ordem_servico": "", "conclusao": "", "data_servico": ""
            })

    return render_template('checklist_gerenciar.html', linhas=linhas)

@checklist_bp.route('/gerenciar', methods=['GET', 'POST'])
def gerenciar_checklists():
    if request.method == 'POST':
        with engine_checklist.connect() as conn:
            for i in range(1, 101):
                placa = request.form.get(f"placa_{i}")
                item = request.form.get(f"item_{i}")

                # Só salva se placa e item estiverem preenchidos
                if placa and item:
                    dados = {
                        "mes": request.form.get(f"mes_{i}"),
                        "data_registro": request.form.get(f"data_registro_{i}"),
                        "placa": placa,
                        "item": item,
                        "fonte": request.form.get(f"fonte_{i}"),
                        "tipo_manutencao": request.form.get(f"tipo_manutencao_{i}"),
                        "status": request.form.get(f"status_{i}"),
                        "ordem_servico": request.form.get(f"ordem_servico_{i}"),
                        "conclusao": request.form.get(f"conclusao_{i}"),
                        "data_servico": request.form.get(f"data_servico_{i}")
                    }

                    # Insere novo registro
                    insert = text("""
                        INSERT INTO checklist (
                            mes, data_registro, placa, item,
                            fonte, tipo_manutencao, status,
                            ordem_servico, conclusao, data_servico
                        ) VALUES (
                            :mes, :data_registro, :placa, :item,
                            :fonte, :tipo_manutencao, :status,
                            :ordem_servico, :conclusao, :data_servico
                        )
                    """)
                    conn.execute(insert, dados)
            conn.commit()
        flash("Dados salvos com sucesso!", "success")
        return redirect('/checklist/gerenciar')

    # GET — carrega os dados existentes
    with engine_checklist.connect() as conn:
        registros = conn.execute(text("SELECT * FROM checklist ORDER BY id")).fetchall()

    # Gera 100 linhas fixas, preenchendo com os dados do banco
    linhas = []
    for i in range(100):
        if i < len(registros):
            r = registros[i]
            linhas.append({
                "mes": r.mes or "",
                "data_registro": r.data_registro or "",
                "placa": r.placa or "",
                "item": r.item or "",
                "fonte": r.fonte or "",
                "tipo_manutencao": r.tipo_manutencao or "",
                "status": r.status or "",
                "ordem_servico": r.ordem_servico or "",
                "conclusao": r.conclusao or "",
                "data_servico": r.data_servico or ""
            })
        else:
            linhas.append({
                "mes": "", "data_registro": "", "placa": "", "item": "",
                "fonte": "", "tipo_manutencao": "", "status": "",
                "ordem_servico": "", "conclusao": "", "data_servico": ""
            })

    return render_template('checklist_gerenciar.html', linhas=linhas)


@checklist_bp.route("/placa/<placa>", methods=["GET", "POST"])
def por_placa(placa):
    if request.method == "POST":
        with engine_checklist.connect() as conn:
            for i in range(1, 101):
                item = request.form.get(f"item_{i}")
                if item:
                    dados = {
                        "mes": request.form.get(f"mes_{i}").upper() if request.form.get(f"mes_{i}") else "",
                        "data_registro": request.form.get(f"data_registro_{i}"),
                        "placa": placa.upper(),  # usa sempre a placa da URL
                        "item": item.upper(),
                        "fonte": request.form.get(f"fonte_{i}", "").upper(),
                        "tipo_manutencao": request.form.get(f"tipo_manutencao_{i}", "").upper(),
                        "status": request.form.get(f"status_{i}", "").upper(),
                        "ordem_servico": request.form.get(f"ordem_servico_{i}", "").upper(),
                        "conclusao": request.form.get(f"conclusao_{i}", "").upper(),
                        "data_servico": request.form.get(f"data_servico_{i}")
                    }

                    id_existente = request.form.get(f"id_{i}")
                    if id_existente:
                        update = text("""
                            UPDATE checklist SET
                                mes = :mes,
                                data_registro = :data_registro,
                                placa = :placa,
                                item = :item,
                                fonte = :fonte,
                                tipo_manutencao = :tipo_manutencao,
                                status = :status,
                                ordem_servico = :ordem_servico,
                                conclusao = :conclusao,
                                data_servico = :data_servico
                            WHERE id = :id
                        """)
                        dados["id"] = id_existente
                        conn.execute(update, dados)
                    else:
                        insert = text("""
                            INSERT INTO checklist (
                                mes, data_registro, placa, item,
                                fonte, tipo_manutencao, status,
                                ordem_servico, conclusao, data_servico
                            ) VALUES (
                                :mes, :data_registro, :placa, :item,
                                :fonte, :tipo_manutencao, :status,
                                :ordem_servico, :conclusao, :data_servico
                            )
                        """)
                        conn.execute(insert, dados)
            conn.commit()
        flash(f"Checklist salvo para a placa {placa.upper()} com sucesso!", "success")
        return redirect(url_for('checklist.por_placa', placa=placa))  # redireciona após salvar

    # ← Aqui está o que faltava: montar as linhas para exibição
    with engine_checklist.connect() as conn:
        registros = conn.execute(text("""
            SELECT * FROM checklist
            WHERE UPPER(placa) = :placa
            ORDER BY data_registro DESC
        """), {"placa": placa.upper()}).fetchall()

    linhas = []
    for i in range(100):
        if i < len(registros):
            r = registros[i]
            linhas.append({
                "id": r.id,
                "mes": r.mes or "",
                "data_registro": r.data_registro or "",
                "placa": r.placa or placa.upper(),
                "item": r.item or "",
                "fonte": r.fonte or "",
                "tipo_manutencao": r.tipo_manutencao or "",
                "status": r.status or "",
                "ordem_servico": r.ordem_servico or "",
                "conclusao": r.conclusao or "",
                "data_servico": r.data_servico or ""
            })
        else:
            linhas.append({
                "id": "",
                "mes": "", "data_registro": "", "placa": placa.upper(), "item": "",
                "fonte": "", "tipo_manutencao": "", "status": "",
                "ordem_servico": "", "conclusao": "", "data_servico": ""
            })

    return render_template("checklist_gerenciar.html", linhas=linhas, placa=placa.upper())



@checklist_bp.route("/placa/<placa>")
def checklist_por_placa(placa):
    with engine_checklist.connect() as conn:
        registros = conn.execute(text("""
            SELECT * FROM checklist
            WHERE UPPER(placa) = :placa
            ORDER BY data_registro DESC
        """), {"placa": placa.upper()}).fetchall()

    # Preenche as 100 linhas
    linhas = []
    for i in range(100):
        if i < len(registros):
            r = registros[i]
            linhas.append({
                "id": r.id,
                "mes": r.mes or "",
                "data_registro": r.data_registro or "",
                "placa": r.placa or "",
                "item": r.item or "",
                "fonte": r.fonte or "",
                "tipo_manutencao": r.tipo_manutencao or "",
                "status": r.status or "",
                "ordem_servico": r.ordem_servico or "",
                "conclusao": r.conclusao or "",
                "data_servico": r.data_servico or ""
            })
        else:
            linhas.append({
                "id": "",
                "mes": "", "data_registro": "", "placa": "", "item": "",
                "fonte": "", "tipo_manutencao": "", "status": "",
                "ordem_servico": "", "conclusao": "", "data_servico": ""
            })

    return render_template("checklist_gerenciar.html", linhas=linhas, placa=placa)

