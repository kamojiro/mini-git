# Project Structure

## Source Code Organization (`src/mini_git/`)

```
src/mini_git/
├── __init__.py          # Package initialization
├── cli.py              # Main CLI entry point with Typer app
├── models.py           # Pydantic data models (IndexEntry, etc.)
├── types.py            # Enums and type definitions (ObjectType)
├── commands/           # Command implementations
│   ├── __init__.py
│   ├── add.py         # AddCommand class
│   └── init.py        # InitCommand class
├── services/          # Business logic layer
│   ├── __init__.py
│   ├── add_service.py     # File staging operations
│   ├── commit_service.py  # Commit operations
│   ├── commit_store.py    # Commit storage
│   ├── repo_context.py    # Repository context management
│   └── tree_store.py      # Tree object storage
├── storage/           # File system operations
│   ├── __init__.py
│   ├── git_dir.py         # Git directory management
│   ├── index_store.py     # Index file operations
│   ├── object_store.py    # Git object storage
│   └── ref_store.py       # Reference storage
└── utils/             # Utility functions
    └── __init__.py
```

## Test Organization (`tests/`)

```
tests/
├── unit/              # Unit tests (isolated components)
│   ├── commands/      # Command layer tests
│   ├── services/      # Service layer tests
│   └── storage/       # Storage layer tests
├── integration/       # Integration tests (multiple components)
└── e2e/              # End-to-end tests (full workflows)
```

## Development & Configuration Files

- `pyproject.toml` - Project metadata, dependencies, and build configuration
- `noxfile.py` - Task automation (linting, formatting)
- `uv.lock` - Dependency lock file
- `.python-version` - Python version specification
- `samples/git_samples/` - Sample Git repositories for testing

## Naming Conventions

### Classes
- **Commands**: `{Action}Command` (e.g., `InitCommand`, `AddCommand`)
- **Services**: `{Domain}Service` (e.g., `AddService`, `CommitService`)
- **Storage**: `{Entity}Store` (e.g., `ObjectStore`, `IndexStore`)
- **Models**: Descriptive names (e.g., `IndexEntry`)

### Files & Modules
- Snake_case for all Python files
- Module names match primary class (e.g., `add_service.py` contains `AddService`)
- Test files prefixed with `test_` and mirror source structure

### Architecture Layers
1. **CLI Layer** (`cli.py`) - User interface and command parsing
2. **Command Layer** (`commands/`) - Command execution and coordination
3. **Service Layer** (`services/`) - Business logic and Git operations
4. **Storage Layer** (`storage/`) - File system and data persistence
5. **Model Layer** (`models.py`, `types.py`) - Data structures and types