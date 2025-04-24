# 🎮 TransROM-IA - AI-Assisted ROM Translation and Dubbing System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-17.0.2-blue.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Development-orange.svg)]()

> 🚀 A comprehensive system for translating and dubbing classic video games using AI. The system is designed to be console-agnostic, starting with GBA support and extensible to other consoles.

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Quick Start](#-quick-start)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Project Overview
TransROM-IA is a comprehensive system for translating and dubbing classic video games using AI. The system is designed to be console-agnostic, starting with GBA support and extensible to other consoles. It combines modern AI technologies with classic game preservation, offering both free and paid service options.

## ⚡ Quick Start

1. **Environment Setup** ⚙️
   - Python 3.9+
   - Node.js 16+
   - Docker
   - Redis
   - PostgreSQL

2. **Installation** 📦
   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/TransROM-IA.git
   cd TransROM-IA

   # Install dependencies
   pip install -r requirements.txt
   npm install

   # Configure environment
   cp .env.example .env
   # Edit .env with your settings

   # Initialize database
   python manage.py migrate
   ```

3. **Development** 💻
   ```bash
   # Start backend server
   python manage.py runserver

   # Start frontend development server
   npm run dev
   ```

## 📚 Documentation

For detailed documentation, please refer to the following files:

- [System Architecture](docs/architecture.md) - Detailed system design and components
- [Development Guide](docs/development.md) - Setup and development guidelines
- [Features and Progress](docs/features.md) - Current features and development progress
- [Credits and Acknowledgments](docs/credits.md) - Project contributors and acknowledgments

## 🤝 Contributing
We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
