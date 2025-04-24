# 🤝 Contributing to TransROM-IA

Thank you for your interest in contributing to TransROM-IA! This document provides guidelines and instructions for contributing to the project.

## 📋 Table of Contents
- [Code of Conduct](#-code-of-conduct)
- [Getting Started](#-getting-started)
- [Development Workflow](#-development-workflow)
- [Code Style](#-code-style)
- [Testing](#-testing)
- [Documentation](#-documentation)
- [Pull Requests](#-pull-requests)
- [Native Modules](#-native-modules)
- [Versioning](#-versioning)

## 📜 Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and considerate of others.

## 🚀 Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/TransROM-IA.git
   cd TransROM-IA
   ```

2. **Set Up Development Environment**
   ```bash
   # Python environment
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate  # Windows

   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt

   # Install native modules
   cd backend/native_modules
   mkdir build && cd build
   cmake ..
   make
   ```

3. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

## 🔄 Development Workflow

1. **Branch Naming Convention**
   - Feature: `feature/v0.x.y-description`
   - Bugfix: `bugfix/v0.x.y-description`
   - Hotfix: `hotfix/v0.x.y-description`
   - Documentation: `docs/description`

2. **Commit Messages**
   - Format: `type(scope): description`
   - Types:
     - `feat`: New feature
     - `fix`: Bug fix
     - `docs`: Documentation
     - `style`: Code style
     - `refactor`: Code refactoring
     - `test`: Testing
     - `chore`: Maintenance

3. **Example Workflow**
   ```bash
   # Create new branch
   git checkout -b feature/v0.1.0-new-feature

   # Make changes
   # ...

   # Stage changes
   git add .

   # Commit
   git commit -m "feat(rom): add new compression algorithm"

   # Push
   git push origin feature/v0.1.0-new-feature
   ```

## 💻 Code Style

### Python
- Follow PEP 8 guidelines
- Use type hints
- Document all public functions
- Keep functions focused and small

### C/C++
- Follow Google C++ Style Guide
- Use C11/C++17 standards
- Document all public interfaces
- Handle memory safely

### JavaScript/TypeScript
- Follow Airbnb Style Guide
- Use TypeScript for type safety
- Document components and functions
- Follow React best practices

## 🧪 Testing

1. **Python Tests**
   ```bash
   # Run all tests
   pytest

   # Run specific test
   pytest tests/test_rom_processor.py

   # Run with coverage
   pytest --cov=backend tests/
   ```

2. **Native Module Tests**
   ```bash
   # Build and run C/C++ tests
   cd backend/native_modules
   mkdir build && cd build
   cmake -DBUILD_TESTING=ON ..
   make
   ctest
   ```

3. **Frontend Tests**
   ```bash
   # Run React tests
   cd frontend
   npm test

   # Run with coverage
   npm test -- --coverage
   ```

## 📚 Documentation

1. **Code Documentation**
   - Use docstrings for Python
   - Use Doxygen for C/C++
   - Use JSDoc for JavaScript/TypeScript

2. **API Documentation**
   - Document all endpoints
   - Include request/response examples
   - Update OpenAPI specification

3. **User Documentation**
   - Update README.md
   - Add/update user guides
   - Document new features

## 🔄 Pull Requests

1. **Before Submitting**
   - Run all tests
   - Update documentation
   - Check code style
   - Ensure no conflicts

2. **PR Template**
   ```markdown
   ## Description
   Brief description of changes

   ## Related Issues
   Fixes #123

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - [ ] Unit tests
   - [ ] Integration tests
   - [ ] Manual testing

   ## Screenshots (if applicable)
   ```

## 🚀 Native Modules

1. **Development Guidelines**
   - Use memory-safe practices
   - Implement proper error handling
   - Follow cross-platform guidelines
   - Document memory management

2. **Building**
   ```bash
   # Windows
   cmake -G "Visual Studio 16 2019" ..
   cmake --build . --config Release

   # Linux/Mac
   cmake ..
   make
   ```

3. **Testing Native Code**
   - Use unit tests
   - Memory leak detection
   - Performance profiling
   - Cross-platform testing

## 📦 Versioning

1. **Version Numbers**
   - Follow Semantic Versioning
   - Update version in:
     - `pyproject.toml`
     - `package.json`
     - Native module headers

2. **Release Process**
   ```bash
   # Create release branch
   git checkout -b release/v0.1.0

   # Update version numbers
   # Run tests
   # Create tag
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   ```

## 🤝 Questions?

If you have any questions about contributing:
- Open an issue
- Join our Discord server
- Contact the maintainers

Thank you for contributing to TransROM-IA! 🎮 