# Architecture Overview

This document describes the modular architecture of the Stream Bill Generator application, which separates concerns while preserving the core computation logic.

## Folder Structure

```
stream-bill-generator/
│
├── app/                        # Streamlit / web front-end
│   ├── __init__.py
│   ├── main.py                 # Streamlit UI entry point
│   ├── ui/                     # UI components
│   ├── routes/                 # Page logic
│   └── onboarding/
│
├── core/                       # Computation logic (DO NOT MODIFY)
│   ├── __init__.py
│   ├── computations/           # Core business logic
│   │   └── bill_processor.py   # Main bill processing logic
│   ├── formulas/               # Mathematical formulas
│   └── validation/             # Data validation logic
│
├── exports/                    # Output formats
│   ├── __init__.py
│   ├── renderers.py            # PDF/XML/CSV rendering functions
│   ├── validators.py            # Schema and compliance validation
│   ├── templates/              # Jinja2/HTML/PDF templates
│   └── renderers/
│
├── data/                       # Databases, static data, reference tables
│   └── __init__.py
│
├── config/                     # Configuration files
│   ├── __init__.py
│   └── settings.py             # Application settings
│
├── tests/                      # pytest test cases
│   └── __init__.py
│
├── scripts/                    # Maintenance, profiling, build scripts
│   └── __init__.py
│
├── templates/                  # Legacy templates (to be migrated)
├── static/                     # Logos, CSS, fonts
└── docs/                       # Documentation
```

## Module Responsibilities

### Core Module (Computation Logic - Untouched)
The `core/` directory contains all computation logic that must not be modified:

- **`core/computations/bill_processor.py`** - Main bill processing logic including:
  - `process_bill()` - Primary function that processes Excel data
  - `safe_float()` - Safe float conversion with error handling
  - `number_to_words()` - Number to words conversion

This logic is extracted directly from `streamlit_app.py` and preserved exactly as-is.

### App Module (User Interface)
The `app/` directory contains all Streamlit UI code:

- **`app/main.py`** - Streamlit application entry point
- **`app/ui/`** - UI components and widgets
- **`app/routes/`** - Page routing logic
- **`app/onboarding/`** - User onboarding flows

### Exports Module (Output Generation)
The `exports/` directory handles all output format generation:

- **`exports/renderers.py`** - PDF, Word, and other document rendering
- **`exports/validators.py`** - Output validation against statutory requirements
- **`exports/templates/`** - Output templates (Jinja2, HTML, etc.)

### Data Module (Data Access)
The `data/` directory handles data storage and retrieval:

- Database models
- Static data files
- Reference tables

### Config Module (Configuration)
The `config/` directory contains application configuration:

- Settings management
- Environment variables
- Branding information

## Import Flow

```
[UI Layer] → [Export Layer] → [Core Computation Layer]
     ↓              ↓                 ↓
[Streamlit] → [Renderers] → [Bill Processor]
```

Example import flow:
```python
# In app/main.py
from core.computations.bill_processor import process_bill
from exports.renderers import generate_pdf, create_word_doc
```

## Benefits of This Architecture

1. **Computation Logic Protection** - Core business logic is firewalled in the `core/` module
2. **Modular Development** - Teams can work on different modules without conflicts
3. **Easy Testing** - Each module can be tested independently
4. **Maintainability** - Clear separation of concerns makes maintenance easier
5. **Scalability** - New features can be added without touching core logic
6. **Backward Compatibility** - Existing functionality is preserved

## Migration Status

- [x] Core computation logic extracted to `core/computations/bill_processor.py`
- [x] Export functionality modularized in `exports/renderers.py`
- [x] Basic architecture structure created
- [ ] UI components to be fully modularized
- [ ] Data access layer to be implemented
- [ ] Configuration management to be implemented
- [ ] Tests to be added

## Development Guidelines

1. **DO NOT modify files in `core/`** - These contain protected computation logic
2. **Add new features in `app/`, `exports/`, or `data/`** - These are the enhancement areas
3. **Follow the import flow** - UI → Exports → Core
4. **Maintain backward compatibility** - Existing functionality must continue to work
5. **Add tests for new features** - All new code should have unit tests

## Future Enhancements

1. **Internationalization** - Add i18n support for multiple languages
2. **Advanced Output Formats** - Add XML, JSON, and other export formats
3. **Performance Optimization** - Add caching and database indexing
4. **Monitoring** - Add telemetry and error tracking
5. **CI/CD** - Implement continuous integration and deployment