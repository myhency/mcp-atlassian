### Detailed Tool Reference

#### Jira Tools

Total: 31 tools

##### Read Operations

#### `batch_get_changelogs`

Get changelogs for multiple Jira issues (Cloud only).

**Required Parameters:**
  - **`issue_ids_or_keys`**: List of Jira issue IDs or keys, e.g.

#### `download_attachments`

Download attachments from a Jira issue.

**Required Parameters:**
  - **`issue_key`**: Jira issue key (e.g., 'PROJ-123')
  - **`target_dir`**: Directory where attachments should be saved

#### `get_agile_boards`

Get jira agile boards by name, project key, or type.

#### `get_all_projects`

Get all Jira projects accessible to the current user.

#### `get_board_issues`

Get all issues linked to a specific board filtered by JQL.

**Required Parameters:**
  - **`board_id`**: The id of the board (e.g., '1001')
  - **`jql`**: JQL query string (Jira Query Language).

#### `get_issue`

Get details of a specific Jira issue including its Epic links and relationship information.

**Required Parameters:**
  - **`issue_key`**: Jira issue key (e.g., 'PROJ-123')

#### `get_project_issues`

Get all issues for a specific Jira project.

**Required Parameters:**
  - **`project_key`**: The project key

#### `get_project_versions`

Get all fix versions for a specific Jira project.

**Required Parameters:**
  - **`project_key`**: Jira project key (e.g., 'PROJ')

#### `get_sprint_issues`

Get jira issues from sprint.

**Required Parameters:**
  - **`sprint_id`**: The id of sprint (e.g., '10001')

#### `get_sprints_from_board`

Get jira sprints from board by state.

**Required Parameters:**
  - **`board_id`**: The id of board (e.g., '1000')

#### `get_user_profile`

Retrieve profile information for a specific Jira user.

**Required Parameters:**
  - **`user_identifier`**: Identifier for the user (e.g., email address 'user@example.com', username 'johndoe', account ID 'accountid:...', or key for Server/DC).

#### `get_worklog`

Get worklog entries for a Jira issue.

**Required Parameters:**
  - **`issue_key`**: Jira issue key (e.g., 'PROJ-123')

#### `search`

Search Jira issues using JQL (Jira Query Language).

**Required Parameters:**
  - **`jql`**: JQL query string (Jira Query Language).

#### `search_fields`

Search Jira fields by keyword with fuzzy match.

##### Write Operations

#### `add_comment`

Add a comment to a Jira issue.

**Required Parameters:**
  - **`issue_key`**: Jira issue key (e.g., 'PROJ-123')
  - **`comment`**: Comment text in Markdown format

#### `add_worklog`

Add a worklog entry to a Jira issue.

**Required Parameters:**
  - **`issue_key`**: Jira issue key (e.g., 'PROJ-123')
  - **`time_spent`**: Time spent in Jira format.

#### `batch_create_issues`

Create multiple Jira issues in a batch.

**Required Parameters:**
  - **`issues`**: JSON array of issue objects.

#### `batch_create_versions`

Batch create multiple versions in a Jira project.

**Required Parameters:**
  - **`project_key`**: Jira project key (e.g., 'PROJ')
  - **`versions`**: JSON array of version objects.

#### `create_issue`

Create a new Jira issue with optional Epic link or parent for subtasks.

**Required Parameters:**
  - **`project_key`**: The JIRA project key (e.g.
  - **`summary`**: Summary/title of the issue
  - **`issue_type`**: Issue type (e.g.

#### `create_issue_link`

Create a link between two Jira issues.

**Required Parameters:**
  - **`link_type`**: The type of link to create (e.g., 'Duplicate', 'Blocks', 'Relates to')
  - **`inward_issue_key`**: The key of the inward issue (e.g., 'PROJ-123')
  - **`outward_issue_key`**: The key of the outward issue (e.g., 'PROJ-456')

#### `create_remote_issue_link`

Create a remote issue link (web link or Confluence link) for a Jira issue.

**Required Parameters:**
  - **`issue_key`**: The key of the issue to add the link to (e.g., 'PROJ-123')
  - **`url`**: The URL to link to (e.g., 'https://example.com/page' or Confluence page URL)
  - **`title`**: The title/name of the link (e.g., 'Documentation Page', 'Confluence Page')

#### `create_sprint`

Create Jira sprint for a board.

**Required Parameters:**
  - **`board_id`**: The id of board (e.g., '1000')
  - **`sprint_name`**: Name of the sprint (e.g., 'Sprint 1')
  - **`start_date`**: Start time for sprint (ISO 8601 format)
  - **`end_date`**: End time for sprint (ISO 8601 format)

#### `create_version`

Create a new fix version in a Jira project.

**Required Parameters:**
  - **`project_key`**: Jira project key (e.g., 'PROJ')
  - **`name`**: Name of the version

#### `delete_issue`

Delete an existing Jira issue.

**Required Parameters:**
  - **`issue_key`**: Jira issue key (e.g.

#### `get_link_types`

Get all available issue link types.

#### `get_transitions`

Get available status transitions for a Jira issue.

**Required Parameters:**
  - **`issue_key`**: Jira issue key (e.g., 'PROJ-123')

#### `link_to_epic`

Link an existing issue to an epic.

**Required Parameters:**
  - **`issue_key`**: The key of the issue to link (e.g., 'PROJ-123')
  - **`epic_key`**: The key of the epic to link to (e.g., 'PROJ-456')

#### `remove_issue_link`

Remove a link between two Jira issues.

**Required Parameters:**
  - **`link_id`**: The ID of the link to remove

#### `transition_issue`

Transition a Jira issue to a new status.

**Required Parameters:**
  - **`issue_key`**: Jira issue key (e.g., 'PROJ-123')
  - **`transition_id`**: ID of the transition to perform.

#### `update_issue`

Update an existing Jira issue including changing status, adding Epic links, updating fields, etc.

**Required Parameters:**
  - **`issue_key`**: Jira issue key (e.g., 'PROJ-123')
  - **`fields`**: Dictionary of fields to update.

#### `update_sprint`

Update jira sprint.

**Required Parameters:**
  - **`sprint_id`**: The id of sprint (e.g., '10001')

#### Confluence Tools

Total: 11 tools

##### Read Operations

#### `get_comments`

Get comments for a specific Confluence page.

**Required Parameters:**
  - **`page_id`**: Confluence page ID (numeric ID, can be parsed from URL, e.g.

#### `get_labels`

Get labels for a specific Confluence page.

**Required Parameters:**
  - **`page_id`**: Confluence page ID (numeric ID, can be parsed from URL, e.g.

#### `get_page`

Get content of a specific Confluence page by its ID, or by its title and space key.

#### `get_page_children`

Get child pages of a specific Confluence page.

**Required Parameters:**
  - **`parent_id`**: The ID of the parent page whose children you want to retrieve

#### `search`

Search Confluence content using simple terms or CQL.

**Required Parameters:**
  - **`query`**: Search query - can be either a simple text (e.g.

#### `search_user`

Search Confluence users using CQL.

**Required Parameters:**
  - **`query`**: Search query - a CQL query string for user search.

##### Write Operations

#### `add_comment`

Add a comment to a Confluence page.

**Required Parameters:**
  - **`page_id`**: The ID of the page to add a comment to
  - **`content`**: The comment content in Markdown format

#### `add_label`

Add label to an existing Confluence page.

**Required Parameters:**
  - **`page_id`**: The ID of the page to update
  - **`name`**: The name of the label

#### `create_page`

Create a new Confluence page.

**Required Parameters:**
  - **`space_key`**: The key of the space to create the page in (usually a short uppercase code like 'DEV', 'TEAM', or 'DOC')
  - **`title`**: The title of the page
  - **`content`**: The content of the page.

#### `delete_page`

Delete an existing Confluence page.

**Required Parameters:**
  - **`page_id`**: The ID of the page to delete

#### `update_page`

Update an existing Confluence page.

**Required Parameters:**
  - **`page_id`**: The ID of the page to update
  - **`title`**: The new title of the page
  - **`content`**: The new content of the page.

