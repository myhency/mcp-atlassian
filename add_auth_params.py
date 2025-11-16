#!/usr/bin/env python3
"""Script to add authentication parameters to all MCP tool functions."""

import re
import sys


# Authentication parameters to add (as strings to insert)
AUTH_PARAMS_JIRA = '''    jira_url: Annotated[
        str | None,
        Field(
            description="(Optional) Jira instance URL (e.g., 'https://mycompany.atlassian.net'). If not provided, uses environment variable JIRA_URL.",
            default=None,
        ),
    ] = None,
    auth_token: Annotated[
        str | None,
        Field(
            description="(Optional) Authentication token (OAuth token, PAT, or API token). If not provided, uses environment variable credentials.",
            default=None,
        ),
    ] = None,
    auth_type: Annotated[
        Literal["oauth", "pat", "basic"] | None,
        Field(
            description="(Optional) Authentication type. Required if auth_token is provided. Choices: 'oauth', 'pat', 'basic'.",
            default=None,
        ),
    ] = None,
    username: Annotated[
        str | None,
        Field(
            description="(Optional) Username/email (required only for 'basic' auth type)",
            default=None,
        ),
    ] = None,'''

AUTH_PARAMS_CONFLUENCE = '''    confluence_url: Annotated[
        str | None,
        Field(
            description="(Optional) Confluence instance URL (e.g., 'https://mycompany.atlassian.net/wiki'). If not provided, uses environment variable CONFLUENCE_URL.",
            default=None,
        ),
    ] = None,
    auth_token: Annotated[
        str | None,
        Field(
            description="(Optional) Authentication token (OAuth token, PAT, or API token). If not provided, uses environment variable credentials.",
            default=None,
        ),
    ] = None,
    auth_type: Annotated[
        Literal["oauth", "pat", "basic"] | None,
        Field(
            description="(Optional) Authentication type. Required if auth_token is provided. Choices: 'oauth', 'pat', 'basic'.",
            default=None,
        ),
    ] = None,
    username: Annotated[
        str | None,
        Field(
            description="(Optional) Username/email (required only for 'basic' auth type)",
            default=None,
        ),
    ] = None,'''

# Logic to add at the beginning of function body
JIRA_LOGIC = '''    # Use provided credentials if all required parameters are present
    if jira_url and auth_token and auth_type:
        config = build_jira_config_from_params(
            jira_url=jira_url,
            auth_token=auth_token,
            auth_type=auth_type,
            username=username,
        )
        jira = JiraFetcher(config=config)
    else:
        jira = await get_jira_fetcher(ctx)'''

CONFLUENCE_LOGIC = '''    # Use provided credentials if all required parameters are present
    if confluence_url and auth_token and auth_type:
        config = build_confluence_config_from_params(
            confluence_url=confluence_url,
            auth_token=auth_token,
            auth_type=auth_type,
            username=username,
        )
        confluence_fetcher = ConfluenceFetcher(config=config)
    else:
        confluence_fetcher = await get_confluence_fetcher(ctx)'''


def add_params_to_function(content: str, service: str = "jira") -> str:
    """Add authentication parameters to all tool functions.

    Args:
        content: The file content
        service: Either 'jira' or 'confluence'

    Returns:
        Modified content
    """
    auth_params = AUTH_PARAMS_JIRA if service == "jira" else AUTH_PARAMS_CONFLUENCE
    auth_logic = JIRA_LOGIC if service == "jira" else CONFLUENCE_LOGIC
    fetcher_call = (
        "jira = await get_jira_fetcher(ctx)"
        if service == "jira"
        else "confluence_fetcher = await get_confluence_fetcher(ctx)"
    )

    # Pattern to match function signatures
    # Matches from "async def function_name(" to ") -> str:"
    # Captures everything including the closing parenthesis
    func_pattern = re.compile(
        r'(@\w+\.tool\([^)]*\)(?:\n@\w+)?)\n'  # Decorator(s)
        r'(async def \w+\([^)]*?'  # Function start
        r'(?:\n.*?)*?'  # Multi-line parameters
        r'\) -> str:)',  # Return type
        re.MULTILINE | re.DOTALL
    )

    modified = content
    functions_modified = []

    # Find all functions
    for match in func_pattern.finditer(content):
        decorator = match.group(1)
        func_signature = match.group(2)
        full_match = match.group(0)

        # Skip if already has auth parameters
        if "auth_token" in func_signature or "jira_url" in func_signature or "confluence_url" in func_signature:
            continue

        # Skip if the function is too short (probably doesn't use fetcher)
        # Find the function name
        func_name_match = re.search(r'async def (\w+)\(', func_signature)
        if not func_name_match:
            continue
        func_name = func_name_match.group(1)

        # Insert auth parameters before the closing parenthesis
        # Find the position before ") -> str:"
        insert_pos = func_signature.rfind(') -> str:')
        if insert_pos == -1:
            continue

        # Check if there's already a trailing comma
        before_paren = func_signature[:insert_pos].rstrip()
        if not before_paren.endswith(','):
            # Add a comma after the last parameter
            modified_sig = func_signature[:insert_pos].rstrip() + ',\n' + auth_params + '\n' + func_signature[insert_pos:]
        else:
            modified_sig = func_signature[:insert_pos] + '\n' + auth_params + '\n' + func_signature[insert_pos:]

        new_full = decorator + '\n' + modified_sig
        modified = modified.replace(full_match, new_full, 1)
        functions_modified.append(func_name)

    # Now add the logic at the beginning of each function body
    # Pattern to find "jira = await get_jira_fetcher(ctx)" or "confluence_fetcher = await get_confluence_fetcher(ctx)"
    # But only in functions that now have auth parameters
    for func_name in functions_modified:
        # Find this specific function's fetcher call
        # Look for the pattern after the function definition
        func_body_pattern = re.compile(
            rf'(async def {func_name}\([^)]*?\) -> str:\s*\n'
            r'    """[^"]*?"""'  # Docstring
            r'\s*\n)'  # End of docstring
            rf'(\s*{re.escape(fetcher_call)})',  # The fetcher call
            re.MULTILINE | re.DOTALL
        )

        match = func_body_pattern.search(modified)
        if match:
            # Replace the fetcher call with the conditional logic
            modified = modified.replace(
                match.group(0),
                match.group(1) + auth_logic,
                1
            )

    return modified, functions_modified


def main():
    if len(sys.argv) < 3:
        print("Usage: python add_auth_params.py <input_file> <service:jira|confluence>")
        sys.exit(1)

    input_file = sys.argv[1]
    service = sys.argv[2].lower()

    if service not in ["jira", "confluence"]:
        print("Service must be 'jira' or 'confluence'")
        sys.exit(1)

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    modified_content, functions = add_params_to_function(content, service)

    # Write back
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(modified_content)

    print(f"Modified {len(functions)} functions in {input_file}:")
    for func in functions:
        print(f"  - {func}")


if __name__ == "__main__":
    main()
