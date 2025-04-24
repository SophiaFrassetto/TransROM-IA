# 🎮 TransROM-IA - AI-Assisted ROM Translation and Dubbing System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-17.0.2-blue.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Development-orange.svg)]()

> 🚀 A comprehensive system for translating and dubbing classic video games using AI. The system is designed to be console-agnostic, starting with GBA support and extensible to other consoles.

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Project Structure](#-project-structure)
- [API Routes](#-api-routes)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [Database Schema](#-database-schema)
- [Frontend Architecture](#-frontend-architecture)
- [AI Processing Pipeline](#-ai-processing-pipeline)
- [Optimization Strategies](#-optimization-strategies)
- [Development Guidelines](#-development-guidelines)
- [Deployment Strategy](#-deployment-strategy)
- [Getting Started](#-getting-started)
- [Next Steps](#-next-steps)
- [Progress Tracking](#-progress-tracking)
- [Credits](#-credits)

## 🎯 Project Overview
TransROM-IA is a comprehensive system for translating and dubbing classic video games using AI. The system is designed to be console-agnostic, starting with GBA support and extensible to other consoles. It combines modern AI technologies with classic game preservation, offering both free and paid service options.

## 📁 Project Structure
```bash
TransROM-IA/
├── backend/                # 🏗️ Backend services
│   ├── api/               # 🌐 API endpoints
│   │   ├── routes/       # 🛣️ API routes
│   │   ├── models/       # 📦 Data models
│   │   └── services/     # ⚙️ Business logic
│   ├── core/             # 🔧 Core processing
│   │   ├── rom/         # 🎮 ROM processing
│   │   ├── text/        # 📝 Text processing
│   │   └── audio/       # 🔊 Audio processing
│   ├── native_modules/  # 🚀 Native C/C++ modules
│   │   ├── compression/ # 📦 Compression algorithms
│   │   │   ├── lz77/   # LZ77 implementation
│   │   │   └── huffman/ # Huffman coding
│   │   ├── encryption/  # 🔒 ROM encryption/decryption
│   │   └── build/       # 🏗️ Build scripts
│   └── database/        # 💾 Database models
├── frontend/             # 🎨 Frontend application
│   ├── src/
│   │   ├── components/  # 🧩 React components
│   │   ├── pages/      # 📄 Next.js pages
│   │   ├── store/      # 📦 Redux store
│   │   └── styles/     # 🎨 CSS modules
│   └── public/         # 📁 Static assets
├── tests/              # 🧪 Test suites
└── docs/              # 📚 Documentation
```

## 🔌 API Routes Structure
```bash
/api
├── auth/                    # 🔐 Authentication
│   ├── POST /login        # 👤 User login
│   └── POST /logout       # 🚪 User logout
├── roms/                   # 🎮 ROM management
│   ├── POST /upload      # 📤 Upload ROM
│   ├── GET /{id}         # 📋 ROM details
│   └── GET /{id}/status  # 📊 Processing status
├── translations/          # 🔄 Translation jobs
│   ├── POST /           # ➕ Create job
│   ├── GET /            # 📋 List jobs
│   ├── GET /{id}        # 📄 Job details
│   └── GET /{id}/download # ⬇️ Download ROM
└── settings/             # ⚙️ User settings
    ├── GET /            # 📋 Get settings
    └── PUT /            # ✏️ Update settings
```

## 🏗️ System Architecture

### 1. Core Design Patterns

#### 🔧 Factory Pattern
- **Purpose**: Create console-specific implementations dynamically
- **Why**: Allows easy addition of new console support without modifying existing code
- **Implementation**: Console factory creates appropriate handler based on ROM analysis
- **Benefits**: 
  - Decoupled console-specific logic
  - Easy to extend for new consoles
  - Centralized console creation

**Example Implementation**:
```python
class ConsoleFactory:
    @staticmethod
    def create_console(rom_path: str, console_type: str) -> ConsoleBase:
        if console_type == "gba":
            return GBAConsole(rom_path)
        elif console_type == "snes":
            return SNESConsole(rom_path)
        raise ValueError(f"Unsupported console type: {console_type}")
```

#### Strategy Pattern
- **Purpose**: Handle different translation and processing methods
- **Why**: Support multiple AI services and processing approaches
- **Implementation**: 
  - Translation strategies (free/paid services)
  - Audio processing strategies
  - Image processing strategies
- **Benefits**:
  - Flexible service switching
  - Easy to add new processing methods
  - Consistent interface across implementations

**Example Implementation**:
```python
class TranslationStrategy:
    def translate(self, text: str, context: dict) -> str:
        raise NotImplementedError

class AITranslationStrategy(TranslationStrategy):
    def __init__(self, model: TranslationModel):
        self.model = model
    
    def translate(self, text: str, context: dict) -> str:
        return self.model.translate(text, context)
```

#### Observer Pattern
- **Purpose**: Track translation progress and system events
- **Why**: Real-time updates and system monitoring
- **Implementation**:
  - Progress tracking
  - System status updates
  - User notifications
- **Benefits**:
  - Real-time feedback
  - Decoupled monitoring
  - Flexible notification system

#### Repository Pattern
- **Purpose**: Abstract data access layer
- **Why**: Consistent data access across different storage types
- **Implementation**:
  - ROM data access
  - Translation storage
  - User preferences
- **Benefits**:
  - Clean separation of concerns
  - Easy to switch storage backends
  - Consistent data access patterns

### 2. Technology Stack

#### Backend Technologies
- **FastAPI** 🚀
  - Async support for better performance
  - Automatic API documentation
  - Type checking and validation
- **SQLAlchemy**: Database ORM
  - Flexible query building
  - Model relationships
  - Transaction management
- **Celery**: Task queue
  - Background processing
  - Task scheduling
  - Distributed processing
- **Redis**: Caching and message broker
  - Fast in-memory storage
  - Pub/sub messaging
  - Session management

#### Frontend Technologies
- **React** ⚛️
  - Component-based architecture
  - Virtual DOM for performance
  - Rich ecosystem
- **Next.js**: React framework
  - Server-side rendering
  - Static site generation
  - API routes
- **Redux**: State management
  - Predictable state updates
  - Middleware support
  - DevTools integration
- **Material-UI**: Component library
  - Consistent design
  - Responsive components
  - Theme customization

#### Infrastructure
- **Docker** 🐳
  - Consistent environments
  - Easy deployment
  - Scalability
- **PostgreSQL**: Database
  - Reliable data storage
  - Advanced querying
  - Data integrity
- **MinIO**: Object storage
  - File management
  - Scalable storage
  - S3 compatibility

### 3. Database Schema

#### ROMs Table
- **Purpose**: Store ROM metadata and processing information
- **Key Fields**:
  - 🆔 ID (Primary Key)
  - 📄 Filename
  - 🎮 Console Type
  - 🌐 Original Language
  - 📊 Processing Status
  - 📅 Creation Date
  - 🔄 Last Update
- **Relationships**:
  - One-to-many with Text Segments
  - One-to-many with Audio Segments
- **Indexes**:
  - Console Type
  - Processing Status
  - Creation Date

**Example Schema**:
```sql
CREATE TABLE roms (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    console_type VARCHAR(50) NOT NULL,
    original_language VARCHAR(10) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Text Segments Table
- **Purpose**: Store extracted and translated text
- **Key Fields**:
  - ID (Primary Key)
  - ROM ID (Foreign Key)
  - Original Text
  - Translated Text
  - Context Information
  - Offset in ROM
  - Translation Status
- **Indexes**:
  - ROM ID
  - Translation Status
  - Text Similarity

**Example Schema**:
```sql
CREATE TABLE text_segments (
    id SERIAL PRIMARY KEY,
    rom_id INTEGER REFERENCES roms(id),
    offset INTEGER NOT NULL,
    original_text TEXT NOT NULL,
    translated_text TEXT,
    context TEXT,
    status VARCHAR(20) NOT NULL
);
```

#### Audio Segments Table
- **Purpose**: Store audio processing information
- **Key Fields**:
  - ID (Primary Key)
  - ROM ID (Foreign Key)
  - Original Audio Path
  - Generated Audio Path
  - Processing Status
  - Audio Format
  - Duration
- **Indexes**:
  - ROM ID
  - Processing Status
  - Audio Format

### 4. Frontend Architecture

#### Layout Structure
- **Base Layout**
  - Header with navigation
  - Main content area
  - Footer
  - Responsive design
  - Theme support

**Component Structure**:
```
components/
├── layout/
│   ├── Header.tsx
│   ├── Footer.tsx
│   └── Sidebar.tsx
├── rom/
│   ├── RomUploader.tsx
│   ├── ConfigurationPanel.tsx
│   └── AdvancedOptions.tsx
├── translations/
│   ├── TranslationList.tsx
│   ├── StatusCard.tsx
│   └── ProgressBar.tsx
└── user/
    ├── UserMenu.tsx
    ├── ProfileSettings.tsx
    └── ApiKeys.tsx
```

#### Screens
1. **Home Screen (ROM Selection)**
   - File upload interface
   - Configuration panel
     - Translation type selection
     - Target language selection
     - AI service selection
     - Advanced options
   - Progress tracking
   - Error handling

2. **Translations Screen**
   - List of translation jobs
   - Status indicators
   - Progress bars
   - Filtering options
   - Download buttons
   - Cancel options

3. **User Profile**
   - API key management
   - Service preferences
   - Notification settings
   - Usage statistics
   - Billing information

4. **Login Screen**
   - Google authentication
   - User registration
   - Password recovery
   - Terms acceptance

#### State Management
- **Global State**
  - User authentication
  - Translation jobs
  - System settings
  - UI preferences

**Example Redux Store**:
```typescript
interface AppState {
  user: {
    isAuthenticated: boolean;
    profile: UserProfile;
    preferences: UserPreferences;
  };
  translations: {
    items: Translation[];
    currentJob: TranslationJob | null;
    status: 'idle' | 'loading' | 'succeeded' | 'failed';
  };
  settings: {
    apiKeys: ApiKeys;
    defaultLanguage: string;
    notificationSettings: NotificationSettings;
  };
}
```

### 5. AI Processing Pipeline

#### Text Translation
- **Free Options**
  - HuggingFace Transformers
    - Multiple language support
    - Offline capability
    - Custom fine-tuning
  - OpenNMT
    - Custom model training
    - Community models
    - Offline processing
  - Argos Translate
    - Completely offline
    - Easy to use
    - Multiple languages

- **Paid Options**
  - Google Translate API
    - High accuracy
    - Wide language support
    - Real-time translation
  - DeepL API
    - High quality
    - Context awareness
    - Formal/informal options

**Example Translation Pipeline**:
```python
class TranslationPipeline:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.translator = AITranslator()
        self.postprocessor = TextPostprocessor()
    
    async def process(self, text: str, context: dict) -> str:
        processed_text = await self.preprocessor.process(text)
        translated_text = await self.translator.translate(processed_text, context)
        final_text = await self.postprocessor.process(translated_text)
        return final_text
```

#### Image Processing
- **Free Options**
  - Tesseract OCR
    - Offline processing
    - Multiple languages
    - Custom training
  - EasyOCR
    - Easy to use
    - Pre-trained models
    - Python integration
  - OpenCV
    - Image preprocessing
    - Text detection
    - Custom algorithms

- **Paid Options**
  - Google Cloud Vision
    - High accuracy
    - Multiple features
    - Cloud processing
  - Amazon Rekognition
    - Text detection
    - Image analysis
    - Face recognition

#### Audio Processing
- **Free Options**
  - Coqui TTS
    - Multiple voice models
    - Offline processing
    - Custom voice training
  - Mozilla TTS
    - Open source
    - Multiple languages
    - Custom voice cloning
  - Festival
    - Classic TTS system
    - Multiple languages
    - Customizable

- **Paid Options**
  - Amazon Polly
    - High quality voices
    - Multiple languages
    - Neural TTS
  - Google Cloud TTS
    - Natural sounding
    - Multiple voices
    - Custom voice

### 6. Optimization Strategies

#### Translation Memory
- **Purpose**: Reuse existing translations
- **Implementation**:
  - In-memory cache
  - Database storage
  - Similarity matching
- **Benefits**:
  - Faster translations
  - Consistent terminology
  - Reduced API calls

**Example Caching Implementation**:
```python
class TranslationCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.ttl = 3600  # 1 hour
    
    async def get(self, key: str) -> Optional[str]:
        return await self.redis.get(key)
    
    async def set(self, key: str, value: str):
        await self.redis.setex(key, self.ttl, value)
```

#### Caching Systems
- **ROM Analysis Cache**
  - 1-hour TTL
  - Redis implementation
  - JSON serialization
- **Translation Cache**
  - 24-hour TTL
  - Context-aware
  - Similarity-based

#### Database Optimizations
- **Indexing Strategy**
  - Text search optimization
  - Status-based queries
  - Relationship queries
- **Partitioning Strategy**
  - By ROM ID
  - By processing status
  - By creation date

#### Performance Monitoring
- **Metrics Collection**
  - Cache hit rates
  - Translation duration
  - Resource usage
  - Error rates
- **Performance Dashboard**
  - Real-time metrics
  - Historical data
  - Alert system

### 7. Development Guidelines

#### Code Organization
- Clean architecture principles
- Modular design
- Type safety
- Documentation
- Testing strategy

#### Error Handling
- Graceful degradation
- User feedback
- Logging system
- Recovery mechanisms

#### Performance Considerations
- Async operations
- Caching strategies
- Resource management
- Load balancing

#### Security Measures
- API key management
- User authentication
- Data encryption
- Access control

### 8. Deployment Strategy

#### Infrastructure
- Docker containers
- Kubernetes orchestration
- Load balancing
- Auto-scaling

#### Monitoring
- Prometheus metrics
- Grafana dashboards
- Log aggregation
- Error tracking

#### Backup Systems
- Database backups
- File storage backups
- Configuration backups
- Disaster recovery

### 9. Extension Points

#### Console Support
- Base console interface
- Plugin system
- Format detection
- Custom handlers

#### Format Support
- Format registry
- Common formats
- Custom formats
- Validation system

### 10. Getting Started

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

### 11. Next Steps

1. **Core Development**
   - Implement GBA support
   - Create translation pipeline
   - Set up audio processing
   - Build web interface

2. **Feature Development**
   - Add console abstraction
   - Implement plugin system
   - Create admin interface
   - Add analytics

3. **Optimization**
   - Performance tuning
   - Resource optimization
   - Cache optimization
   - Database optimization

4. **Documentation**
   - API documentation
   - User guides
   - Developer guides
   - Architecture diagrams

## 📊 Progress Tracking

### 🎮 Core Features
- [ ] Project Setup
  - [ ] Repository initialization
  - [ ] Basic project structure
  - [ ] Development environment setup
  - [ ] CI/CD pipeline
  - [ ] Documentation setup

- [ ] Backend Development
  - [ ] API Framework setup
  - [ ] Database models
  - [ ] Authentication system
  - [ ] File upload system
  - [ ] Translation service
  - [ ] Audio processing service
  - [ ] Image processing service

- [ ] Frontend Development
  - [ ] Basic layout
  - [ ] Authentication pages
  - [ ] ROM upload interface
  - [ ] Translation management
  - [ ] User settings
  - [ ] Progress tracking
  - [ ] Download system

- [ ] AI Integration
  - [ ] Text translation models
  - [ ] Image processing models
  - [ ] Audio generation models
  - [ ] Optimization systems
  - [ ] Caching mechanisms

### 🕹️ Console Support

#### Game Boy Advance (GBA)
- [ ] ROM Analysis
  - [ ] Text extraction
  - [ ] Audio extraction
  - [ ] Image extraction
  - [ ] Pointer table analysis
- [ ] Translation Pipeline
  - [ ] Text translation
  - [ ] Image translation
  - [ ] Audio dubbing
- [ ] ROM Generation
  - [ ] Text injection
  - [ ] Image injection
  - [ ] Audio injection

#### Super Nintendo (SNES)
- [ ] ROM Analysis
  - [ ] Text extraction
  - [ ] Audio extraction
  - [ ] Image extraction
  - [ ] Pointer table analysis
- [ ] Translation Pipeline
  - [ ] Text translation
  - [ ] Image translation
  - [ ] Audio dubbing
- [ ] ROM Generation
  - [ ] Text injection
  - [ ] Image injection
  - [ ] Audio injection

#### Nintendo Entertainment System (NES)
- [ ] ROM Analysis
  - [ ] Text extraction
  - [ ] Audio extraction
  - [ ] Image extraction
  - [ ] Pointer table analysis
- [ ] Translation Pipeline
  - [ ] Text translation
  - [ ] Image translation
  - [ ] Audio dubbing
- [ ] ROM Generation
  - [ ] Text injection
  - [ ] Image injection
  - [ ] Audio injection

### 🛠️ Infrastructure
- [ ] Development Environment
  - [ ] Docker setup
  - [ ] Database setup
  - [ ] Cache system
  - [ ] File storage
- [ ] Production Environment
  - [ ] Server setup
  - [ ] Load balancing
  - [ ] Monitoring
  - [ ] Backup system

### 📚 Documentation
- [ ] User Documentation
  - [ ] Installation guide
  - [ ] User manual
  - [ ] Troubleshooting guide
- [ ] Developer Documentation
  - [ ] API documentation
  - [ ] Architecture guide
  - [ ] Contribution guide
- [ ] Console-specific Documentation
  - [ ] GBA guide
  - [ ] SNES guide
  - [ ] NES guide

## 🚀 Native Module Integration

#### C/C++ Integration
- **Purpose**: Handle performance-critical operations
- **Key Components**:
  - ROM compression/decompression
  - Encryption/decryption
  - Binary data manipulation
  - Memory-intensive operations

#### Implementation Strategy
```c
// Example: LZ77 Compression Module
#include <Python.h>
#include <stdint.h>
#include <stdlib.h>

// Memory-safe buffer handling
typedef struct {
    uint8_t* data;
    size_t size;
    size_t capacity;
} SafeBuffer;

// Python-C interface
static PyObject* compress_lz77(PyObject* self, PyObject* args) {
    Py_buffer input;
    SafeBuffer output;
    
    if (!PyArg_ParseTuple(args, "y*", &input)) {
        return NULL;
    }
    
    // Initialize output buffer with safety checks
    output.capacity = input.len * 2; // Conservative estimate
    output.data = (uint8_t*)malloc(output.capacity);
    if (!output.data) {
        PyBuffer_Release(&input);
        PyErr_NoMemory();
        return NULL;
    }
    
    // Compression logic here
    
    // Clean up and return
    PyObject* result = PyBytes_FromStringAndSize((char*)output.data, output.size);
    free(output.data);
    PyBuffer_Release(&input);
    return result;
}
```

#### Memory Management
- **Python-C Interface**:
  - Use Py_buffer for safe memory handling
  - Implement reference counting
  - Clean up resources properly
  - Handle exceptions safely

- **Cross-Platform Support**:
  - CMake build system
  - Platform-specific optimizations
  - Conditional compilation
  - Automated testing

#### Build System
```cmake
# CMakeLists.txt example
cmake_minimum_required(VERSION 3.10)
project(TransROM-IA_Native)

# Platform-specific settings
if(WIN32)
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

# Native modules
add_library(compression SHARED
    src/compression/lz77.c
    src/compression/huffman.c
)

# Python extension
Python_add_library(py_compression MODULE
    src/python/compression_module.c
)

# Link dependencies
target_link_libraries(py_compression PRIVATE compression)
```

## 📦 Versioning System

### Semantic Versioning (SemVer)
Format: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

#### Version History
- **v0.1.0**: Initial release
  - Basic ROM processing
  - GBA support
  - Text extraction
- **v0.2.0**: Native modules
  - C/C++ integration
  - Compression support
  - Performance improvements
- **v0.3.0**: Multi-console
  - SNES support
  - NES support
  - Enhanced processing

#### Development Workflow
1. Feature branches: `feature/v0.x.y-description`
2. Release branches: `release/v0.x.y`
3. Hotfix branches: `hotfix/v0.x.y`

#### Version Tags
```bash
# Create version tag
git tag -a v0.1.0 -m "Initial release"

# Push tag
git push origin v0.1.0
```

## 👥 Credits

### 🧑‍💻 Project Lead
- **Sophia de Angelo Frassetto**
  - Project conception and architecture
  - System design and implementation
  - AI integration strategy
  - Quality assurance and testing

### 🤖 AI Development Partners
This project was developed in collaboration with AI tools, which contributed to:
- **Code Development**
  - Architecture design and patterns
  - Implementation suggestions
  - Code review and optimization
  - Testing strategies

- **Documentation**
  - Technical documentation
  - API specifications
  - User guides
  - Architecture diagrams

- **Problem Solving**
  - Algorithm optimization
  - Performance improvements
  - Debugging assistance
  - Best practices implementation

### 🎮 Community Support
- **Retro Gaming Community**
  - ROM format documentation
  - Console-specific knowledge
  - Testing and feedback
  - Feature suggestions

- **Open Source Contributors**
  - Code contributions
  - Bug reports
  - Feature requests
  - Documentation improvements

### 🛠️ Tools and Technologies
- **Development Tools**
  - GitHub for version control
  - Docker for containerization
  - VS Code for development
  - AI coding assistants
  - CMake for native builds
  - GCC/Clang for compilation

- **Core Technologies**
  - Python for high-level logic
  - C/C++ for performance-critical operations
  - SQLAlchemy for database
  - React for frontend
  - Redis for caching

- **Native Development**
  - C/C++ compilers
  - Python C API
  - Memory profiling tools
  - Cross-platform build systems
  - Performance monitoring

### 🙏 Acknowledgments
Special thanks to:
- The retro gaming preservation community
- Open source developers and maintainers
- AI research and development teams
- Game translation enthusiasts
- Beta testers and early adopters

## 🤝 Contributing
We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

> 💡 Note: This project represents a successful collaboration between human expertise and AI capabilities, combining the best of both worlds to create a powerful ROM translation system. The AI assistance was crucial in accelerating development while maintaining high code quality and comprehensive documentation.
