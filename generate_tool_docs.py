#!/usr/bin/env python3
"""Generate tool documentation from MCP schemas."""

import json
from typing import Dict, List, Any

def categorize_tools(tools: List[Dict[str, Any]]) -> tuple[List[Dict], List[Dict]]:
    """Categorize tools into Jira and Confluence."""
    jira_tools = []
    confluence_tools = []

    # Tools that appear in both services need special handling
    for tool in tools:
        params = tool['inputSchema'].get('properties', {})

        # Check for service-specific URL parameters
        has_jira_url = 'jira_url' in params
        has_confluence_url = 'confluence_url' in params

        if has_jira_url and not has_confluence_url:
            jira_tools.append(tool)
        elif has_confluence_url and not has_jira_url:
            confluence_tools.append(tool)
        elif has_jira_url and has_confluence_url:
            # Should not happen, but handle it
            print(f"Warning: Tool {tool['name']} has both URL types")
            jira_tools.append(tool)
        else:
            # No URL params, check description
            desc = tool['description'].lower()
            if 'confluence' in desc:
                confluence_tools.append(tool)
            else:
                jira_tools.append(tool)

    return jira_tools, confluence_tools

def format_tool_doc(tool: Dict[str, Any]) -> str:
    """Format a single tool's documentation."""
    name = tool['name']

    # Extract first line of description
    desc_lines = tool['description'].strip().split('\n')
    short_desc = desc_lines[0].strip()

    # Get required parameters
    schema = tool['inputSchema']
    required = schema.get('required', [])
    properties = schema.get('properties', {})

    # Build parameter list
    params = []
    for param_name in required:
        if param_name in properties:
            param_info = properties[param_name]
            param_desc = param_info.get('description', '').strip()

            # Clean up description - take first line or sentence
            if param_desc:
                # Split by newline first
                lines = param_desc.split('\n')
                first_line = lines[0].strip()

                # If first line ends with a sentence, use it
                if '. ' in first_line:
                    param_desc = first_line.split('. ')[0] + '.'
                elif first_line.endswith('.'):
                    param_desc = first_line
                else:
                    # Take up to first period or 150 chars
                    if '. ' in param_desc:
                        param_desc = param_desc.split('. ')[0] + '.'
                    else:
                        param_desc = (param_desc[:150] + '...') if len(param_desc) > 150 else param_desc

                # Remove common prefixes
                param_desc = param_desc.replace('(Optional) ', '').replace('(Required) ', '')

            params.append(f"  - **`{param_name}`**: {param_desc}")

    # Build markdown
    md = f"#### `{name}`\n\n"
    md += f"{short_desc}\n\n"
    if params:
        md += "**Required Parameters:**\n"
        md += "\n".join(params) + "\n\n"

    return md

def generate_documentation(tools: List[Dict[str, Any]]) -> str:
    """Generate complete tools documentation."""
    jira_tools, confluence_tools = categorize_tools(tools)

    # Sort by name
    jira_tools.sort(key=lambda x: x['name'])
    confluence_tools.sort(key=lambda x: x['name'])

    doc = "### Detailed Tool Reference\n\n"

    # Jira Tools
    doc += "#### Jira Tools\n\n"
    doc += f"Total: {len(jira_tools)} tools\n\n"

    # Categorize by operation type
    read_tools = []
    write_tools = []

    for tool in jira_tools:
        name = tool['name']
        if any(keyword in name for keyword in ['create', 'update', 'delete', 'add', 'link', 'transition', 'remove', 'batch_create']):
            write_tools.append(tool)
        else:
            read_tools.append(tool)

    doc += "##### Read Operations\n\n"
    for tool in read_tools:
        doc += format_tool_doc(tool)

    doc += "##### Write Operations\n\n"
    for tool in write_tools:
        doc += format_tool_doc(tool)

    # Confluence Tools
    doc += "#### Confluence Tools\n\n"
    doc += f"Total: {len(confluence_tools)} tools\n\n"

    # Categorize by operation type
    read_tools = []
    write_tools = []

    for tool in confluence_tools:
        name = tool['name']
        if any(keyword in name for keyword in ['create', 'update', 'delete', 'add']):
            write_tools.append(tool)
        else:
            read_tools.append(tool)

    doc += "##### Read Operations\n\n"
    for tool in read_tools:
        doc += format_tool_doc(tool)

    doc += "##### Write Operations\n\n"
    for tool in write_tools:
        doc += format_tool_doc(tool)

    return doc

def main():
    with open('mcp_tools_schemas.json', 'r') as f:
        tools = json.load(f)

    documentation = generate_documentation(tools)

    # Print summary
    jira_tools, confluence_tools = categorize_tools(tools)
    print(f"Generated documentation for {len(tools)} tools:")
    print(f"  - Jira: {len(jira_tools)}")
    print(f"  - Confluence: {len(confluence_tools)}")

    # Write to file
    with open('TOOLS_DOCUMENTATION.md', 'w') as f:
        f.write(documentation)

    print("\nDocumentation written to TOOLS_DOCUMENTATION.md")

if __name__ == '__main__':
    main()
