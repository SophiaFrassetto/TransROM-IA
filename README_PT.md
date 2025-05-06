# 🎮 TransROM-IA

> :us: [English version](README.md)

<div align="center">

![TransROM-IA Logo](https://via.placeholder.com/150)

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-Latest-black.svg)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Development-orange.svg)]()

**Uma plataforma inovadora para tradução e dublagem de ROMs de videogames usando Inteligência Artificial**

[Tecnologias](#-tecnologias) •
[Plano de Estrutura do Projeto](#️-plano-de-estrutura-do-projeto-modular--escalavel) •
[Instalação](#-instalação) •
[Como Executar](#-como-executar) •
[Documentação da API](#-documentação-da-api) •
[Autenticação & Segurança](#-autenticação-e-segurança) •
[Contribuição](#-contribuição) •
[Licença](#-licença)

</div>

## 🗂️ Plano de Estrutura do Projeto (Modular & Escalável)

> **Abaixo está a estrutura atual e planejada do TransROM-IA, refletindo a nova organização. Este plano é pensado para modularidade, escalabilidade e suporte a múltiplos consoles, e pode evoluir conforme o projeto cresce.**

```
TransROM-IA/
│
├── backend/
│   ├── apis_app/                # App FastAPI, API, models, schemas, banco de dados, serviços
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── main.py
│   │   └── ...
│   │
│   ├── console_manipulation/    # Código modular, core e específico de console
│   │   ├── core/                # Lógica genérica e reutilizável (agnóstica de console)
│   │   ├── consoles/            # Módulos específicos de console (ex: gba/)
│   │   ├── native/              # Módulos nativos para performance (C/C++/C#)
│   │   ├── tables/              # Tabelas de caracteres por console
│   │   ├── scripts/             # Scripts utilitários, conversores, etc
│   │   ├── tests/               # Testes unitários e de integração
│   │   ├── cli/                 # Interface de linha de comando (Python)
│   │   ├── docs/                # Documentação técnica (GBA.md, GBA_PT.md, etc)
│   │   └── ...
│   │
│   ├── alembic/                 # Migrações do banco de dados
│   ├── logs/                    # Arquivos de log
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── ...
│
├── frontend/                    # Todo o frontend (Next.js, React, etc)
│   ├── src/
│   ├── components/
│   ├── pages/
│   ├── styles/
│   └── ...
│
├── roms_examples/               # ROMs de exemplo para testes
├── README.md                    # Versão em inglês deste README
├── README_PT.md                 # Esta versão em português
└── ...                          # Arquivos de configuração do projeto (package.json, etc)
```

### Pontos-chave
- **backend/apis_app/**: Toda a lógica de API, banco de dados e negócios (FastAPI, models, schemas, etc).
- **backend/console_manipulation/**: Todo o código modular, core e específico de console para manipulação de ROMs, extensível para múltiplos consoles.
- **frontend/**: Todo o código da interface web (Next.js, React, etc).
- **roms_examples/**: ROMs de exemplo para testes e desenvolvimento.
- **README.md**: Versão em inglês deste README.

> Esta estrutura foi pensada para fácil manutenção, extensibilidade e separação clara entre lógica de API/negócio e manipulação de ROM/consoles.

---

## 📋 Sobre o Projeto

TransROM-IA é uma plataforma avançada que combina tecnologias modernas de IA com a preservação de jogos clássicos. O sistema foi projetado para ser agnóstico em relação ao console, começando com suporte a GBA e sendo extensível para outras plataformas. Nossa solução oferece:

- 🤖 Tradução automática de textos usando IA
- 🎙️ Dublagem com vozes sintéticas de alta qualidade
- 🎮 Suporte inicial para ROMs de GBA
- 🔄 Sistema extensível para outros consoles
- 🌐 Interface web moderna e intuitiva

---

## 🚀 Tecnologias

### Backend
- [Python 3.13](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [AsyncPG](https://magicstack.github.io/asyncpg/)
- [Python-Jose](https://python-jose.readthedocs.io/)
- [Passlib](https://passlib.readthedocs.io/)

### Frontend
- [Next.js](https://nextjs.org/)
- [TypeScript](https://www.typescriptlang.org/)
- [TailwindCSS](https://tailwindcss.com/)

---

## 💻 Instalação

### Pré-requisitos
- Python 3.13+
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

---

## 🎯 Como Executar

### Backend

1. Aplique as migrações do banco de dados
```bash
cd backend
alembic upgrade head
```

2. Inicie o servidor de desenvolvimento
```bash
uvicorn apis_app.main:app --reload --host 0.0.0.0 --port 8000
```
O backend estará disponível em `http://localhost:8000`

### Frontend

1. Inicie o servidor de desenvolvimento
```bash
cd frontend
npm run dev
```
O frontend estará disponível em `http://localhost:3000`

---

## 📝 Documentação da API

A documentação da API está disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 🔐 Autenticação e Segurança

O sistema utiliza:
- JWT (JSON Web Tokens) para autenticação
- Bcrypt para hash de senhas
- HTTPS para comunicação segura
- Validação de dados com Pydantic
- Proteção contra ataques comuns (CSRF, XSS)

---

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor, abra issues ou envie pull requests para melhorias, correções de bugs ou novas funcionalidades.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">
Feito com ❤️ pela equipe TransROM-IA
</div> 