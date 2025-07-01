from flask import current_app
from app.models import Veiculo, whatsapp_numeros
from whatsapp import enviar_mensagem_whatsapp
from datetime import datetime
import requests
from app.models import whatsapp_numeros



def gerar_resumo_veiculos():
    with current_app.app_context():
        veiculos = Veiculo.query.all()
        em_alerta = [
            v for v in veiculos if (
                v.km_para_preventiva is not None and v.km_para_preventiva <= 5000 or
                v.km_para_intermediaria is not None and v.km_para_intermediaria <= 5000
            )
        ]

        if not em_alerta:
            return None  # nada para enviar

        mensagem = f"📅 ALERTA de Manutenção - {datetime.today().strftime('%d/%m/%Y')}\n\n"
        for v in em_alerta:
            mensagem += (
                f"🚛 *{v.placa}* ({v.motorista})\n"
                f"• KM Atual: {v.km_atual} km\n"
                f"• Preventiva: {v.km_para_preventiva or 'N/D'} km\n"
                f"• Intermediária: {v.km_para_intermediaria or 'N/D'} km\n\n"
            )

        return mensagem

def disparar_alerta():
    mensagem = gerar_resumo_veiculos()
    if mensagem:
        print("📨 MENSAGEM GERADA:\n", mensagem)
        for numero in whatsapp_numeros:
            sucesso = enviar_mensagem_whatsapp(numero, mensagem)
            print(f'Enviado para {numero}: {"✔️" if sucesso else "❌"}')
    else:
        print("✅ Nenhum veículo precisa de manutenção no momento.")

def enviar_alerta_manutencao(numero, placa, condutor, preventiva, intermediaria, km_atual):
    token = "EAAKA1BO7HoQBO6VSlpcqpDvkAVKd3oNDxC8XHRHxcqBTszeNVB362YN4rpMybru9sfJiybpJbyRsVuNSTdIqZC4BhKKa1P1BY2342MCnvHuc9BURq3QF7zYcDb0BeH5Pqq83wTJheJZAEnFCFpLZBwBa8bU4fRCOdXlOjXyfqKvOdZC6RPEQEZAmhoVBMLMZCny7wE1FD5tmXsHXBQZCjw8CLADR65enJ0caPJYibOT7zUC9wZDZD"
    phone_number_id = "700570819805323"

    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "template",
        "template": {
            "name": "alerta_manutencao",
            "language": { "code": "pt_BR" },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": placa},
                        {"type": "text", "text": condutor},
                        {"type": "text", "text": str(preventiva)},
                        {"type": "text", "text": str(intermediaria)},
                        {"type": "text", "text": str(km_atual)}
                    ]
                }
            ]
        }
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(f"Enviado para {numero}: {response.status_code}")
    print(response.text)

    return response.status_code == 200


def disparar_alertas_reais():
    with current_app.app_context():
        veiculos = Veiculo.query.all()
        em_alerta = [
            v for v in veiculos if (
                v.km_para_preventiva is not None and v.km_para_preventiva <= 5000 or
                v.km_para_intermediaria is not None and v.km_para_intermediaria <= 5000
            )
        ]
        
        for v in em_alerta:
            for numero in whatsapp_numeros:
                print(f"📋 {v.placa} → motorista={v.motorista}, prev={v.km_para_preventiva}, inter={v.km_para_intermediaria}, atual={v.km_atual}")
                
                sucesso = enviar_alerta_manutencao(
                    numero,
                    v.placa,
                    v.motorista or "DESCONHECIDO",
                    v.km_para_preventiva or "N/D",
                    v.km_para_intermediaria or "N/D",
                    v.km_atual or 0
                )

                print(f"✅ Envio para {v.placa}: {'OK' if sucesso else 'FALHOU'}")


def extrair_dados():
    from flask import current_app
    with current_app.app_context():
        veiculos = Veiculo.query.all()
        em_alerta = [
            v for v in veiculos if (
                v.km_para_preventiva is not None and v.km_para_preventiva <= 5000 or
                v.km_para_intermediaria is not None and v.km_para_intermediaria <= 5000
            )
        ]
        linhas = []
        for v in em_alerta:
            linhas.append({
                "placa": v.placa,
                "motorista": v.motorista,
                "km_atual": f"{v.km_atual:,}".replace(",", ".") + " km",
                "preventiva": f"{v.km_para_preventiva or 'N/D'} km",
                "intermediaria": f"{v.km_para_intermediaria or 'N/D'} km"
            })
        return linhas

