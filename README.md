# 🎮 TransROM-IA

<div align="center">

![TransROM-IA Logo](https://via.placeholder.com/150)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Latest-blue.svg)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Development-orange.svg)]()

**Uma plataforma inovadora para tradução e dublagem de ROMs de videogames usando Inteligência Artificial**

[Tecnologias](#-tecnologias) •
[Instalação](#-instalação) •
[Como Executar](#-como-executar) •
[Contribuição](#-contribuição) •
[Licença](#-licença)

</div>

## 📋 Sobre o Projeto

TransROM-IA é uma plataforma avançada que combina tecnologias modernas de IA com preservação de jogos clássicos. O sistema foi projetado para ser agnóstico em relação aos consoles, começando com suporte para GBA e sendo extensível para outras plataformas. Nossa solução oferece:

- 🤖 Tradução automática de textos usando IA
- 🎙️ Dublagem com vozes sintéticas de alta qualidade
- 🎮 Suporte inicial para ROMs de GBA
- 🔄 Sistema extensível para outros consoles
- 🌐 Interface web moderna e intuitiva

## 🚀 Tecnologias

### Backend
- [Python 3.9+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)

### Frontend
- [React](https://reactjs.org/)
- [Next.js](https://nextjs.org/)
- [TypeScript](https://www.typescriptlang.org/)
- [TailwindCSS](https://tailwindcss.com/)

## 💻 Instalação

### Pré-requisitos
- Python 3.9+
- Node.js 16+
- PostgreSQL
- Git

### Configuração do Ambiente

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/TransROM-IA.git
cd TransROM-IA
```

2. Configure o ambiente virtual Python
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

3. Instale as dependências do backend
```bash
cd backend
pip install -r requirements.txt
```

4. Instale as dependências do frontend
```bash
cd frontend
npm install
```

5. Configure as variáveis de ambiente
```bash
# Na pasta backend
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

## 🎯 Como Executar

### Backend

1. Aplique as migrações do banco de dados
```bash
cd backend
alembic upgrade head
```

2. Inicie o servidor de desenvolvimento
```bash
uvicorn app.main:app --reload
```
O backend estará disponível em `http://localhost:8000`

### Frontend

1. Inicie o servidor de desenvolvimento
```bash
cd frontend
npm run dev
```
O frontend estará disponível em `http://localhost:3000`

## 📝 API Documentation

A documentação da API está disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">
Feito com ❤️ pela equipe TransROM-IA
</div>
