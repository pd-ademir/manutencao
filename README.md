# 🛠️ Sistema de Gestão de Almoxarifado

Sistema web desenvolvido em Flask para gerenciamento de veículos, manutenções preventivas e unidades operacionais.

---

## ✨ Funcionalidades

- Cadastro de veículos e suas respectivas unidades
- Painel de manutenção com destaque visual para revisões vencidas
- Gerenciamento de usuários com controle de acesso (Master/Comum)
- Registro de logs de ações (para usuários Master)
- Interface responsiva com menu dinâmico e rodapé fixo
- Autenticação segura com redirecionamento automático para login

---

## 📦 Tecnologias Utilizadas

- Python + Flask
- SQLAlchemy (ORM)
- SQLite como banco local
- Jinja2 para templates HTML
- Flask-Login para autenticação
- Flask-Migrate para versionamento do banco de dados

---

## 🚀 Executando Localmente

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Rodar aplicação
flask run


---

Você pode colar esse conteúdo num arquivo `README.md`, fazer um `git add README.md`, `git commit -m "Adiciona README"` e depois `git push`.

Se quiser, também posso gerar badges automáticos, um `requirements.txt` baseado no seu `venv` ou até preparar um deploy gratuito com o PythonAnywhere ou Render. Só dizer que o time da retaguarda está a postos 🧰😄