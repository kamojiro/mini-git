# Technology Stack

## Build System & Package Management
- **Build Backend**: Hatchling (modern Python packaging)
- **Package Manager**: uv (fast Python package installer)
- **Virtual Environment**: uv-managed environments
- **Python Version**: >= 3.12

## Core Dependencies
- **Pydantic**: Data validation and settings management using Python type annotations
- **Typer**: Modern CLI framework for building command-line applications

## Development Tools
- **Testing**: pytest for unit and integration testing
- **Linting & Formatting**: Ruff for fast Python linting and code formatting
- **Type Checking**: Pyright for static type analysis
- **Task Runner**: Nox with uv backend for automation

## Common Commands

### Development Setup
```bash
# Install dependencies
uv sync --all-extras --frozen

# Activate virtual environment
source .venv/bin/activate
```

### Code Quality
```bash
# Run linting and formatting
uv run nox -s ruff

# Run tests
uv run pytest

# Type checking (via IDE or manual)
uv run pyright

# ci
uv run nox
```

### Build & Install
```bash
# Install in development mode
uv pip install -e .

# Use the CLI
uv run mgit --help
```

## Architecture Patterns
- **Command Pattern**: Commands in `commands/` directory implement business logic
- **Service Layer**: Services in `services/` handle core Git operations
- **Storage Layer**: Storage classes in `storage/` manage file system operations
- **Pydantic Models**: Immutable data models with validation
- **Type Safety**: Extensive use of Python type hints and enums