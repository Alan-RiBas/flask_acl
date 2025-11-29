# ACL API -- Flask

Este projeto é uma API em Flask com sistema de ACL (Access Control
List).

## 🚀 Instalação

### 1. Clone o repositório

``` bash
git clone https://seu-repo.git
cd nome-do-projeto
```

### 2. Crie e ative um ambiente virtual

``` bash
python3 -m venv venv
source venv/bin/activate       # Linux / Mac
venv\Scripts\activate        # Windows
```

### 3. Instale as dependências

``` bash
pip install -r requirements.txt
```

## ⚙️ Configuração

Crie um arquivo `.env` na raiz do projeto:

    FLASK_ENV=development
    SECRET_KEY=sua_chave_secreta_aqui
    JWT_SECRET_KEY=sua_chave_jwt_aqui
    DATABASE_URI=postgresql://usuario:senha@localhost:5432/sua_base

## 🗄️ Banco de Dados

``` bash
flask create-db
```

## ▶️ Executando o servidor

``` bash
flask run --port=8000
```
