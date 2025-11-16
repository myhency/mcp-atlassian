# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MCP Atlassian is a Model Context Protocol (MCP) server that bridges Atlassian products (Jira and Confluence) with AI language models. It's distributed as a Docker image and supports both Cloud and Server/Data Center deployments with multiple authentication methods (API tokens, Personal Access Tokens, OAuth 2.0).

## Development Commands

### Environment Setup

```bash
# Install dependencies using uv
uv sync
uv sync --frozen --all-extras --dev

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate.ps1

# Set up pre-commit hooks
pre-commit install

# Copy environment configuration
cp .env.example .env
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=mcp_atlassian

# Run specific test file
uv run pytest tests/unit/test_exceptions.py

# Run specific test function
uv run pytest tests/unit/test_exceptions.py::test_specific_function

# Run tests matching a pattern
uv run pytest -k "jira"
```

### Code Quality

```bash
# Run all pre-commit checks
pre-commit run --all-files

# Run specific checks
pre-commit run ruff --all-files
pre-commit run pyright --all-files
```

### Building and Running

```bash
# Build Docker image
docker build -t mcp-atlassian:local .

# Run locally for development (stdio mode)
uv run mcp-atlassian -vv

# Run with HTTP transport for testing
uv run mcp-atlassian --transport sse --port 9000 -vv
# or
uv run mcp-atlassian --transport streamable-http --port 9000 -vv

# Test with MCP Inspector
npx @modelcontextprotocol/inspector uv --directory . run mcp-atlassian -vv
```

## Architecture

### High-Level Structure

The project uses a modular, mixin-based architecture:

1. **Entry Point** (`src/mcp_atlassian/__init__.py`): CLI handling using Click, environment setup
2. **Server Layer** (`src/mcp_atlassian/servers/`):
   - `main.py`: FastMCP server setup with lifespan management
   - `jira.py`: Jira MCP tool definitions
   - `confluence.py`: Confluence MCP tool definitions
   - `dependencies.py`: Shared dependency injection and request context handling
3. **Client Layer** (`src/mcp_atlassian/{jira,confluence}/`): API interaction implementations organized as mixins
4. **Models** (`src/mcp_atlassian/models/`): Pydantic models for Jira and Confluence data structures
5. **Preprocessing** (`src/mcp_atlassian/preprocessing/`): Content transformation for Jira and Confluence responses
6. **Utilities** (`src/mcp_atlassian/utils/`): Shared utilities for auth, logging, environment handling, etc.

### Key Architectural Patterns

**Mixin-Based Client Design**: Both `JiraFetcher` and `ConfluenceFetcher` are composed from multiple mixins (e.g., `IssuesMixin`, `SearchMixin`, `PagesMixin`). Each mixin focuses on a specific domain:
- `src/mcp_atlassian/jira/__init__.py`: `JiraFetcher` inherits from `ProjectsMixin`, `IssuesMixin`, `SearchMixin`, etc.
- `src/mcp_atlassian/confluence/__init__.py`: `ConfluenceFetcher` inherits from `SearchMixin`, `PagesMixin`, `CommentsMixin`, etc.

**Authentication Handling**: Multi-layered authentication supporting Cloud and Server/DC:
- **Config classes** (`JiraConfig`, `ConfluenceConfig`) in `{jira,confluence}/config.py` determine auth type from environment
- **Auth precedence**: Username/API Token (Cloud) → Personal Access Token (Server/DC) → OAuth (Cloud)
- **OAuth support**: Standard OAuth 2.0 flow with refresh tokens, plus "Bring Your Own Token" (BYOT) mode for external token management
- **Multi-Cloud OAuth**: When `ATLASSIAN_OAUTH_ENABLE=true`, requests can provide per-user OAuth tokens via headers

**Request Context Management** (`servers/dependencies.py`):
- Handles per-request authentication (supports multi-user scenarios via HTTP headers)
- Manages client instances (reuses or creates based on auth context)
- Caches configurations using TTLCache for performance

**Content Preprocessing** (`preprocessing/`):
- `base.py`: Abstract `Preprocessor` class defining the interface
- `jira.py`: Transforms Jira API responses (e.g., simplifying issue objects, formatting fields)
- `confluence.py`: Converts Confluence storage format to readable markdown

**FastMCP Server Pattern**:
- Uses `@asynccontextmanager` for lifespan management (loading configs, cleanup)
- Middleware for per-request context (`RequestAuthContextMiddleware`)
- Tools are conditionally loaded based on `READ_ONLY_MODE` and `ENABLED_TOOLS` filters

### Authentication Architecture

The project supports four authentication methods with automatic detection:

1. **API Token** (Cloud - Recommended): `JIRA_USERNAME` + `JIRA_API_TOKEN`
2. **Personal Access Token** (Server/DC): `JIRA_PERSONAL_TOKEN`
3. **OAuth 2.0 Standard**: Full OAuth client setup with token refresh (requires `--oauth-setup` wizard)
4. **OAuth BYOT**: Pre-existing access tokens managed externally (`ATLASSIAN_OAUTH_ACCESS_TOKEN`)

Detection logic in `{jira,confluence}/config.py`:
- Checks for username/API token first (basic auth)
- Falls back to Personal Access Token for Server/DC URLs
- Then checks OAuth configuration (BYOT or standard client credentials)
- Multi-Cloud mode: minimal server config, per-request auth via headers

### Tool Registration and Filtering

Tools are defined in `servers/{jira,confluence}.py` and registered with FastMCP. The system supports:
- **Read-only mode**: When `READ_ONLY_MODE=true`, only read operations are available
- **Tool filtering**: `ENABLED_TOOLS` environment variable restricts which tools are exposed
- **Dynamic tool loading**: Tools are conditionally included based on service availability and configuration

## Code Style and Standards

- **Line length**: 88 characters (enforced by ruff)
- **Type annotations**: Required for all functions; use `type[T]`, `str | None`, `list[str]`, `dict[str, Any]`
- **Docstrings**: Google-style format for all public functions, classes, and methods
- **Linting**: Ruff with strict rules (see `pyproject.toml` for configuration)
- **Type checking**: Pyright (preferred over mypy)
- **Testing**: pytest with session-scoped fixtures, factory patterns, and mock utilities in `tests/utils/`

## Important Patterns to Follow

### Adding a New Jira Tool

1. Implement the method in the appropriate mixin in `src/mcp_atlassian/jira/` (e.g., `issues.py` for issue operations)
2. Define the tool in `src/mcp_atlassian/servers/jira.py` using `@jira_mcp.tool()` decorator
3. Use `get_jira_config_and_fetcher()` dependency for auth context
4. Add preprocessing if needed in `src/mcp_atlassian/preprocessing/jira.py`
5. Mark as read-only operation if applicable (exclude from write operations)

### Adding a New Confluence Tool

Same pattern as Jira but using:
- Mixins in `src/mcp_atlassian/confluence/`
- Tool definitions in `src/mcp_atlassian/servers/confluence.py`
- Dependency: `get_confluence_config_and_fetcher()`
- Preprocessing in `src/mcp_atlassian/preprocessing/confluence.py`

### Testing Strategy

The test suite uses a factory pattern with session-scoped fixtures (see `tests/README.md`):
- **Unit tests**: Mock external dependencies, test individual components
- **Integration tests**: Test against mock Atlassian API responses
- **Factory fixtures**: `make_jira_issue()`, `make_confluence_page()` for customizable test data
- **Session fixtures**: `session_jira_field_definitions`, `session_confluence_spaces` for shared data
- **Environment fixtures**: `clean_environment`, `oauth_environment` for auth testing

### Handling Sensitive Data

- Use `mask_sensitive()` from `utils/logging.py` to mask tokens/passwords in logs
- Custom headers are automatically masked in debug logs
- OAuth tokens are stored in `~/.mcp-atlassian/` and should never be committed
- All proxy credentials are masked in logs

## Environment Variables Reference

Critical environment variables (see `.env.example` for full list):

**Service URLs**:
- `JIRA_URL`: Jira instance URL
- `CONFLUENCE_URL`: Confluence instance URL

**Authentication** (choose one method per service):
- `JIRA_USERNAME` + `JIRA_API_TOKEN` (Cloud)
- `JIRA_PERSONAL_TOKEN` (Server/DC)
- OAuth variables: `ATLASSIAN_OAUTH_CLIENT_ID`, `ATLASSIAN_OAUTH_CLIENT_SECRET`, `ATLASSIAN_OAUTH_CLOUD_ID`, etc.

**Filtering**:
- `JIRA_PROJECTS_FILTER`: Comma-separated project keys
- `CONFLUENCE_SPACES_FILTER`: Comma-separated space keys
- `ENABLED_TOOLS`: Comma-separated tool names

**Behavior**:
- `READ_ONLY_MODE`: Set to "true" to disable write operations
- `MCP_VERBOSE`: Enable debug logging
- `MCP_LOGGING_STDOUT`: Log to stdout instead of stderr

**Network**:
- `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`, `SOCKS_PROXY`
- Service-specific overrides: `JIRA_HTTPS_PROXY`, `CONFLUENCE_NO_PROXY`
- `JIRA_SSL_VERIFY`, `CONFLUENCE_SSL_VERIFY`: SSL verification (default: true)
- `JIRA_CUSTOM_HEADERS`, `CONFLUENCE_CUSTOM_HEADERS`: Custom HTTP headers (comma-separated `key=value` pairs)

## Release Process

This project uses semantic versioning with automated versioning from git tags:
- Version is derived from git tags via `uv-dynamic-versioning`
- Pre-commit hooks enforce code quality
- GitHub Actions run tests on pull requests
- Docker images are published to `ghcr.io/sooperset/mcp-atlassian`
