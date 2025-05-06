# 🎮 TransROM-IA

> :brazil: [Versão em Português](README_PT.md)

<div align="center">

![TransROM-IA Logo](https://via.placeholder.com/150)

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-Latest-black.svg)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Development-orange.svg)]()

**An innovative platform for translation and dubbing of videogame ROMs using Artificial Intelligence**

[Technologies](#-technologies) •
[Project Structure Plan](#️-project-structure-plan-modular--scalable) •
[Installation](#-installation) •
[How to Run](#-how-to-run) •
[API Documentation](#-api-documentation) •
[Authentication & Security](#-authentication-and-security) •
[Contribution](#-contribution) •
[License](#-license)

</div>

## 🗂️ Project Structure Plan (Modular & Scalable)

> **Below is the current and planned folder structure for TransROM-IA, reflecting the new organization. This plan is designed for modularity, scalability, and multi-console support, and may evolve as the project grows.**

```
TransROM-IA/
│
├── backend/
│   ├── apis_app/                # FastAPI app, API, models, schemas, database, services
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── main.py
│   │   └── ...
│   │
│   ├── console_manipulation/    # Modular, core, and console-specific code
│   │   ├── core/                # Generic, reusable logic (console-agnostic)
│   │   ├── consoles/            # Console-specific modules (e.g., gba/)
│   │   ├── native/              # Native modules for performance (C/C++/C#)
│   │   ├── tables/              # Character tables by console
│   │   ├── scripts/             # Utility scripts, converters, etc
│   │   ├── tests/               # Unit and integration tests
│   │   ├── cli/                 # Command-line interface (Python)
│   │   ├── docs/                # Technical documentation (GBA.md, GBA_PT.md, etc)
│   │   └── ...
│   │
│   ├── alembic/                 # Database migrations
│   ├── logs/                    # Log files
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── ...
│
├── frontend/                    # All frontend (Next.js, React, etc)
│   ├── src/
│   ├── components/
│   ├── pages/
│   ├── styles/
│   └── ...
│
├── roms_examples/               # Example ROMs for testing
├── README.md
├── README_PT.md                 # Portuguese version of this README
└── ...                          # Project root files (package.json, etc)
```

### Key Points
- **backend/apis_app/**: All API, database, and business logic (FastAPI, models, schemas, etc).
- **backend/console_manipulation/**: All modular, core, and console-specific code for ROM manipulation, extensible for multiple consoles.
- **frontend/**: All web interface code (Next.js, React, etc).
- **roms_examples/**: Example ROMs for testing and development.
- **README_PT.md**: Portuguese version of this README.

> This structure is designed for easy maintenance, extensibility, and clear separation between API/business logic and ROM/console manipulation code.

---

## 📋 About the Project

TransROM-IA is an advanced platform that combines modern AI technologies with classic game preservation. The system is designed to be console-agnostic, starting with GBA support and extensible to other platforms. Our solution offers:

- 🤖 Automatic text translation using AI
- 🎙️ High-quality synthetic voice dubbing
- 🎮 Initial support for GBA ROMs
- 🔄 Extensible system for other consoles
- 🌐 Modern and intuitive web interface

---

## 🚀 Technologies

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

## 💻 Installation

### Prerequisites
- Python 3.13+
- Node.js 16+
- PostgreSQL
- Git

### Environment Setup

1. Clone the repository
```bash
git clone https://github.com/seu-usuario/TransROM-IA.git
cd TransROM-IA
```

2. Set up the Python virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

3. Install backend dependencies
```bash
cd backend
pip install -r requirements.txt
```

4. Install frontend dependencies
```bash
cd frontend
npm install
```

5. Configure environment variables
```bash
# In the backend folder
cp .env.example .env
# Edit the .env file with your settings
```

---

## 🎯 How to Run

### Backend

1. Apply database migrations
```bash
cd backend
alembic upgrade head
```

2. Start the development server
```bash
uvicorn apis_app.main:app --reload --host 0.0.0.0 --port 8000
```
The backend will be available at `http://localhost:8000`

### Frontend

1. Start the development server
```bash
cd frontend
npm run dev
```
The frontend will be available at `http://localhost:3000`

---

## 📝 API Documentation

API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 🔐 Authentication and Security

The system uses:
- JWT (JSON Web Tokens) for authentication
- Bcrypt for password hashing
- HTTPS for secure communication
- Data validation with Pydantic
- Protection against common attacks (CSRF, XSS)

---

## 🤝 Contribution

Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new features.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<div align="center">
Made with ❤️ by the TransROM-IA team
</div>
