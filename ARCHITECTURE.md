# MediScan Architecture

## Overview

MediScan is a Python-based application that provides barcode scanning and product management with a focus on medicines and perishable items. The architecture follows a layered design pattern with clear separation of concerns.

## Architecture Layers

```
┌─────────────────────────────────────────────────┐
│           Application Layer (CLI)                │
│              app.py, commands                    │
└─────────────────────────────────────────────────┘
                      │
┌─────────────────────────────────────────────────┐
│              AI Layer                            │
│    Recipe Generator, Medicine Analyzer,          │
│         Counterfeit Detector                     │
└─────────────────────────────────────────────────┘
                      │
┌─────────────────────────────────────────────────┐
│            Service Layer                         │
│   Product, Verification, Expiry,                 │
│   Notification, Barcode Scanner                  │
└─────────────────────────────────────────────────┘
                      │
┌─────────────────────────────────────────────────┐
│            Model Layer                           │
│   Product, Medicine, PerishableItem,             │
│   ManufacturingLog, Notification                 │
└─────────────────────────────────────────────────┘
                      │
┌─────────────────────────────────────────────────┐
│           Data Storage Layer                     │
│         JSON files, File System                  │
└─────────────────────────────────────────────────┘
```

## Core Components

### 1. Application Layer (`app.py`)

**Purpose**: Entry point and CLI interface

**Key Classes**:
- `MediScanApp`: Main application controller
  - Initializes all services
  - Handles CLI commands
  - Coordinates between services
  - Displays results to user

**Responsibilities**:
- Command parsing and routing
- User interface (CLI with Rich library)
- Service coordination
- Error handling and user feedback

### 2. Model Layer (`src/models/`)

**Purpose**: Data structures and business entities

**Key Classes**:

#### Product (`product.py`)
- Base class for all products
- Fields: barcode, name, manufacturer, dates, batch_number
- Methods: expiry calculation, validation, serialization

#### Medicine (`product.py`)
- Extends Product
- Additional fields: dosage, active ingredients, side effects, interactions
- Medicine-specific validation

#### PerishableItem (`product.py`)
- Extends Product
- Additional fields: storage temp, nutritional info, allergens
- Perishable-specific logic

#### ManufacturingLog (`manufacturing_log.py`)
- Verification data from manufacturers
- Fields: batch info, quality checks, certification
- Validation methods

#### Notification (`notification.py`)
- Alert and reminder system
- Types: expiry warnings, recalls, interactions
- Priority levels and scheduling

### 3. Service Layer (`src/services/`)

**Purpose**: Business logic and operations

#### BarcodeScanner (`barcode_scanner.py`)
- **Responsibilities**:
  - Camera-based scanning (optional)
  - Image-based scanning (optional)
  - Barcode validation
  - Barcode generation

- **Dependencies**: opencv-python, pyzbar (optional)
- **Design**: Graceful degradation if dependencies missing

#### ProductService (`product_service.py`)
- **Responsibilities**:
  - Product CRUD operations
  - Search and filtering
  - Category-based queries
  - JSON persistence

- **Storage**: JSON files in `data/products/`
- **Design**: In-memory cache with persistence

#### VerificationService (`verification_service.py`)
- **Responsibilities**:
  - Manufacturing log management
  - Product verification
  - Recall checking
  - Counterfeit flagging

- **Storage**: CSV/JSON in `data/manufacturing_logs/`
- **Design**: Multi-format log support

#### ExpiryTracker (`expiry_tracker.py`)
- **Responsibilities**:
  - Expiry date monitoring
  - Urgency categorization
  - Usage recommendations
  - Priority calculations

- **Design**: Configurable warning thresholds
- **Features**: Medicine vs. perishable differentiation

#### NotificationService (`notification_service.py`)
- **Responsibilities**:
  - Notification creation and management
  - Priority-based filtering
  - Scheduled notifications
  - Notification lifecycle

- **Storage**: JSON in `data/`
- **Design**: Event-driven notification system

### 4. AI Layer (`src/ai/`)

**Purpose**: AI-powered features and analysis

#### RecipeGenerator (`recipe_generator.py`)
- **Responsibilities**:
  - Recipe generation from ingredients
  - Priority-based ingredient selection
  - Dietary preference handling
  - Fallback recipe templates

- **AI Integration**: OpenAI API (optional)
- **Design**: Works with/without AI API

#### MedicineAnalyzer (`medicine_analyzer.py`)
- **Responsibilities**:
  - Drug interaction detection
  - Safety analysis
  - Adherence tracking
  - Dosage recommendations

- **Knowledge Base**: Built-in interaction database
- **AI Integration**: Optional AI enhancement
- **Design**: Rule-based with AI augmentation

#### CounterfeitDetector (`counterfeit_detector.py`)
- **Responsibilities**:
  - Counterfeit risk assessment
  - Pattern recognition
  - Batch analysis
  - Verification checklist generation

- **Algorithm**: Multi-factor risk scoring
- **Design**: Heuristic-based with confidence levels

### 5. Utility Layer (`src/utils/`)

#### Config (`config.py`)
- Environment variable management
- Configuration validation
- Default values

#### DataLoader (`data_loader.py`)
- Sample data generation
- CSV/JSON import
- Data initialization

## Data Flow

### Product Scanning Flow

```
User Input (Barcode)
    ↓
BarcodeScanner.validate_barcode()
    ↓
ProductService.get_product()
    ↓
VerificationService.verify_product()
    ↓
CounterfeitDetector.analyze_product()
    ↓
ExpiryTracker.check_expiry_status()
    ↓
Display Results to User
```

### Expiry Notification Flow

```
Scheduled Task
    ↓
ProductService.list_products()
    ↓
ExpiryTracker.get_expiring_products()
    ↓
For each expiring product:
    ↓
NotificationService.create_expiry_warning()
    ↓
NotificationService.send_pending_notifications()
```

### Medicine Interaction Flow

```
User Request
    ↓
ProductService.get_medicines()
    ↓
MedicineAnalyzer.check_interactions()
    ↓
For each medicine pair:
    ↓
Check active ingredients
    ↓
Check contraindications
    ↓
Check known interactions
    ↓
Return interaction results
```

### Recipe Generation Flow

```
User Request
    ↓
ProductService.get_perishable_items()
    ↓
Filter by expiry urgency
    ↓
RecipeGenerator.generate_recipe()
    ↓
If AI available:
    Call OpenAI API
Else:
    Use fallback templates
    ↓
Return recipe suggestions
```

## Design Patterns

### 1. Service Pattern
- Services encapsulate business logic
- Services are stateless or manage their own state
- Services depend on models, not vice versa

### 2. Repository Pattern
- ProductService acts as repository
- Abstracts data storage details
- In-memory caching with persistence

### 3. Strategy Pattern
- AI components use strategy pattern
- Fallback strategies when AI unavailable
- Configurable behavior via environment

### 4. Observer Pattern (implicit)
- Expiry tracker with callbacks
- Notification system for events
- Extensible event handling

### 5. Factory Pattern
- Model creation from dictionaries
- Product type polymorphism
- Flexible instantiation

## Data Storage

### Current Implementation: JSON Files

**Advantages**:
- Simple and portable
- Human-readable
- No database dependencies
- Easy backup and version control

**Storage Locations**:
- Products: `data/products/products.json`
- Logs: `data/manufacturing_logs/*.{json,csv}`
- Notifications: `data/notifications.json`

**Future Considerations**:
- SQLite for better querying
- PostgreSQL for production
- Redis for caching
- Cloud storage integration

## Security Considerations

### Current Security Measures

1. **API Key Protection**
   - Environment variables for secrets
   - .env excluded from git
   - No hardcoded credentials

2. **Data Validation**
   - Input validation on all user inputs
   - Barcode format validation
   - Date range validation

3. **Counterfeit Detection**
   - Multi-factor verification
   - Manufacturing log validation
   - Risk scoring system

4. **Local Data Storage**
   - Data stored locally by default
   - No automatic cloud sync
   - User controls data

### Future Security Enhancements

1. Encrypted data storage
2. User authentication
3. Role-based access control
4. Audit logging
5. Secure API communication

## Scalability Considerations

### Current Limitations
- In-memory product cache (limited by RAM)
- Single-user design
- Local file storage
- Synchronous operations

### Scalability Path

1. **Phase 1: Database Integration**
   - Replace JSON with SQLite
   - Add connection pooling
   - Implement pagination

2. **Phase 2: Multi-User Support**
   - Add user authentication
   - Implement data isolation
   - Add concurrent access handling

3. **Phase 3: Distributed System**
   - API server (REST/GraphQL)
   - Microservices architecture
   - Cloud storage
   - Message queue for notifications

4. **Phase 4: Enterprise Scale**
   - Load balancing
   - Horizontal scaling
   - Caching layer (Redis)
   - CDN for static assets

## Extension Points

### Adding New Product Types

1. Create new class extending `Product`
2. Add type-specific fields
3. Update `ProductService._dict_to_product()`
4. Add type-specific display in `app.py`

### Adding New AI Features

1. Create new class in `src/ai/`
2. Implement with fallback logic
3. Add configuration options
4. Integrate into main app

### Adding New Notification Types

1. Add enum to `NotificationType`
2. Create factory method in `NotificationService`
3. Add display handling in CLI

### Adding New Data Sources

1. Create importer in `utils/`
2. Implement data transformation
3. Add to initialization flow

## Testing Strategy

### Current Testing
- Manual CLI testing
- Sample data verification
- Import validation

### Recommended Testing

1. **Unit Tests**
   - Model validation
   - Service logic
   - AI algorithms
   - Utility functions

2. **Integration Tests**
   - Service interactions
   - Data persistence
   - End-to-end flows

3. **Performance Tests**
   - Large dataset handling
   - Concurrent operations
   - Memory usage

4. **Security Tests**
   - Input validation
   - SQL injection (when using DB)
   - XSS prevention (when adding web UI)

## Dependencies

### Core Dependencies (Required)
- python-dateutil: Date manipulation
- python-dotenv: Configuration
- colorama: Terminal colors
- rich: CLI formatting

### Optional Dependencies
- opencv-python: Camera scanning
- pyzbar: Barcode decoding
- python-barcode: Barcode generation
- pillow: Image processing
- openai: AI features

### Development Dependencies
- pytest: Testing framework
- black: Code formatting
- pylint: Linting
- mypy: Type checking

## Configuration Management

### Environment Variables
- `OPENAI_API_KEY`: AI features
- `DATABASE_URL`: Storage location
- `ENABLE_NOTIFICATIONS`: Feature toggle
- `NOTIFICATION_LEAD_TIME_DAYS`: Warning threshold
- `VERIFICATION_STRICT_MODE`: Verification behavior

### Configuration Hierarchy
1. Environment variables
2. .env file
3. Default values in Config class

## Performance Considerations

### Current Performance
- O(n) product search
- O(1) product lookup by barcode
- O(n²) interaction checking
- In-memory operations (fast)

### Optimization Opportunities
1. Index barcode lookups
2. Cache interaction checks
3. Lazy load product details
4. Batch operations
5. Async I/O for file operations

## Monitoring and Logging

### Current Logging
- Print statements for user feedback
- Error messages to console

### Future Monitoring
1. Structured logging (JSON)
2. Log levels (DEBUG, INFO, WARNING, ERROR)
3. Log rotation
4. Application metrics
5. Health checks
6. Performance monitoring

## Deployment

### Current: Local Installation
```bash
pip install -r requirements.txt
python app.py
```

### Future: Containerization
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### Production Deployment
1. Docker container
2. Kubernetes orchestration
3. Cloud deployment (AWS/GCP/Azure)
4. CI/CD pipeline
5. Blue-green deployment

## Conclusion

MediScan is designed as a modular, extensible application with clear separation of concerns. The architecture supports both current requirements and future enhancements while maintaining simplicity and maintainability.

Key architectural strengths:
- ✅ Modular design
- ✅ Clear layering
- ✅ Graceful degradation
- ✅ Extensible structure
- ✅ Flexible storage
- ✅ AI integration ready
- ✅ Security conscious

The architecture positions MediScan for growth from a single-user CLI application to a potential enterprise-grade distributed system.
