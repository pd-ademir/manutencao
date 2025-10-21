# app/permissoes.py

PERMISSOES = {
    "master": {
        "visualizar": True,
        "editar_km": True,
        "alterar_dados": True,
        "admin": True
    },
    "comum": {
        "visualizar": True,
        "editar_km": True,
        "alterar_dados": True,
        "admin": False
    },
    "visualizador": {
        "visualizar": True,
        "editar_km": False,
        "alterar_dados": False,
        "admin": False
    },
    "teste": {
        "visualizar": True,
        "editar_km": False,
        "alterar_dados": False,
        "admin": False
    }
}


def tem_permissao(tipo_usuario, acao):
    return PERMISSOES.get(tipo_usuario, {}).get(acao, False)
