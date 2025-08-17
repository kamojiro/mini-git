# Testing Strategy

This document explains the testing strategy and structure for the mini-git project.

## Test Categories

### Unit Tests (`tests/unit/`)

Unit tests focus on testing individual classes and functions in isolation using mocks for dependencies. They follow the principle of testing one unit of code at a time.

**Key characteristics:**
- Use `pytest-mock` (MockerFixture) to mock dependencies
- Test single classes/functions in isolation
- Fast execution
- No file system operations (except for test data creation)
- Mock all external dependencies

**Example:**
```python
def test_add_object_reads_file_and_stores_blob(mocker: MockerFixture, tmp_path: Path):
    # Create test file
    test_file = tmp_path / "test.txt"
    test_content = b"Hello, World!\n"
    test_file.write_bytes(test_content)

    # Mock the ObjectStore dependency
    object_store = mocker.Mock(spec=ObjectStore)
    mock_object_store_write = mocker.patch.object(
        object_store, 'write', return_value='1234567890abcdef1234567890abcdef12345678'
    )
    service = AddService(object_store)

    # Test the service method
    oid = service.add_object(test_file)

    # Verify behavior
    assert isinstance(oid, str)
    assert len(oid) == 40
    mock_object_store_write.assert_called_once_with(ObjectType.BLOB, test_content)
```

### Integration Tests (`tests/integration/`)

Integration tests verify that multiple components work correctly together. They test the interaction between different layers of the application.

**Key characteristics:**
- Test multiple components working together
- Real implementations (no mocking of internal components)
- Test data flows between layers
- Verify end-to-end functionality within the application

**Example:**
```python
def test_add_service_with_object_store_integration(tmp_path: Path):
    # Test AddService working with real ObjectStore
    test_file = tmp_path / "test.txt"
    test_content = b"Hello, World!\n"
    test_file.write_bytes(test_content)

    git_dir = tmp_path / ".git"
    object_store = ObjectStore(git_dir)  # Real ObjectStore
    service = AddService(object_store)   # Real AddService

    oid = service.add_object(test_file)

    # Verify the integration worked
    obj_type, content = object_store.read(oid)
    assert obj_type == "blob"
    assert content == test_content
```

### End-to-End Tests (`tests/e2e/`)

E2E tests verify the complete functionality by running the actual `mgit` command and comparing results with real `git` behavior.

**Key characteristics:**
- Execute the full `mgit` CLI command using subprocess
- Compare results with actual `git` commands
- Test the complete user workflow
- Verify compatibility with git standards

**Example:**
```python
def test_mgit_add_single_file_matches_git(tmp_path: Path):
    # Create test file
    test_file = tmp_path / "hello.txt"
    test_content = "Hello, World!\n"
    test_file.write_text(test_content)

    # Initialize both mgit and git repos
    mgit_result = run_command(["uv", "run", "mgit", "init"], tmp_path)
    git_result = run_command(["git", "init"], tmp_path)

    # Get hashes from both systems
    git_hash = get_git_object_hash(test_file, tmp_path)
    mgit_hash = get_mgit_object_hash(test_file, tmp_path)

    # Verify they match
    assert mgit_hash == git_hash
```

## Test Structure

```
tests/
├── unit/              # Unit tests (isolated components)
│   ├── commands/      # Command layer tests
│   ├── services/      # Service layer tests
│   ├── storage/       # Storage layer tests
│   └── test_models.py # Model tests
├── integration/       # Integration tests (multiple components)
│   ├── test_add_workflow.py      # Add workflow integration
│   └── test_cli_integration.py   # CLI integration
└── e2e/              # End-to-end tests (full workflows)
    ├── test_cli_e2e.py     # CLI E2E tests
    └── test_git_add.py     # Git compatibility tests
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test categories
uv run pytest tests/unit/        # Unit tests only
uv run pytest tests/integration/ # Integration tests only
uv run pytest tests/e2e/         # E2E tests only

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/unit/services/test_add_service.py -v
```

## Test Guidelines

### Unit Tests
- Mock all external dependencies using `mocker.Mock(spec=ClassName)`
- Test edge cases and error conditions
- Keep tests fast and isolated
- Use descriptive test names that explain the behavior being tested

### Integration Tests
- Use real implementations of internal components
- Test realistic scenarios and data flows
- Verify that components work together correctly
- Focus on interfaces between layers

### E2E Tests
- Test complete user workflows
- Compare behavior with real git when possible
- Use subprocess to run actual CLI commands
- Test both success and failure scenarios

## Benefits of This Structure

1. **Fast Feedback**: Unit tests run quickly and catch basic issues
2. **Confidence**: Integration tests ensure components work together
3. **Compatibility**: E2E tests verify git compatibility
4. **Maintainability**: Clear separation makes tests easier to understand and maintain
5. **Debugging**: Failed tests at different levels help identify where issues occur