# 🏗️ System Architecture

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

## 🎯 Core Design Patterns

### 🔧 Factory Pattern
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

### Strategy Pattern
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

### Observer Pattern
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

### Repository Pattern
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

## 💾 Database Schema

### ROMs Table
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

### Text Segments Table
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

### Audio Segments Table
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

## 🎨 Frontend Architecture

### Layout Structure
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

### State Management
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

## 🚀 Native Module Integration

### C/C++ Integration
- **Purpose**: Handle performance-critical operations
- **Key Components**:
  - ROM compression/decompression
  - Encryption/decryption
  - Binary data manipulation
  - Memory-intensive operations

**Example Implementation**:
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

### Build System
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