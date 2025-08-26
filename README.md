# Django Base API

## 🎯 Intuito do Projeto

Este projeto tem como objetivo servir como **esqueleto base** para futuras APIs REST construídas com Django REST framework. Ele foi pensado para acelerar o início de novos projetos de backend, já incluindo configurações essenciais e boas práticas.

### ✅ Funcionalidades Incluídas

- **Estrutura modular** de aplicativos para fácil escalabilidade.
- **Autenticação JWT** (login, logout, refresh de token).
- **CRUD de usuários** via app `accounts`.
- **Conexão com PostgreSQL** configurada via arquivo `.env`.
- **Documentação automática da API** usando Swagger (drf-yasg).
- **Painel administrativo do Django** pronto para uso.
- Organização de pastas para `views`, `serializers`, `models` e `urls` visando manutenibilidade.
- Configuração com variáveis de ambiente para segurança e flexibilidade.
- Pronto para deploy em ambientes de desenvolvimento e produção.

---

## 🛠️ Tutorial de Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/Pedro-Pesssoa/Django_base_api.git
```

### 2. Criar e ativar o ambiente virtual
Lembre de verificar em que pasta você está, caso não esteja dentro pasta do projeto basta utilizar o comando ```cd [nome da pasta]```

Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Instalar dependências
Edite um arquivo ```.env_exemplo``` para ```.env``` e edite as informações conforme indicado no arquivo

### 5. Instalar dependências
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Criar superusuário
```bash
python manage.py createsuperuser
```

### 7. Rodar o servidor de desenvolvimento
```bash
python manage.py runserver
```
Acessar a API:
- Painel Administrativo: http://127.0.0.1:8000/admin/
- Documentação Swagger: http://127.0.0.1:8000/swagger/
