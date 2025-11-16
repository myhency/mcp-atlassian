"""Configuration builder utilities for creating configs from function parameters."""

import logging
from typing import Literal

from mcp_atlassian.confluence.config import ConfluenceConfig
from mcp_atlassian.jira.config import JiraConfig

logger = logging.getLogger("mcp-atlassian.utils.config_builder")


def build_jira_config_from_params(
    jira_url: str,
    auth_token: str,
    auth_type: Literal["oauth", "pat", "basic"] = "oauth",
    username: str | None = None,
    ssl_verify: bool = True,
) -> JiraConfig:
    """Build a JiraConfig from function parameters.

    Args:
        jira_url: Jira instance URL (e.g., 'https://mycompany.atlassian.net')
        auth_token: Authentication token (OAuth token, PAT, or API token)
        auth_type: Authentication type ('oauth', 'pat', or 'basic')
        username: Username/email (required for 'basic' auth)
        ssl_verify: Whether to verify SSL certificates (default: True)

    Returns:
        JiraConfig instance configured with the provided parameters

    Raises:
        ValueError: If required parameters are missing for the auth type
    """
    logger.debug(
        f"Building JiraConfig from params: url={jira_url}, auth_type={auth_type}, username={username}"
    )

    if auth_type == "basic":
        if not username:
            raise ValueError(
                "username is required for 'basic' authentication type"
            )
        return JiraConfig(
            url=jira_url,
            auth_type="basic",
            username=username,
            api_token=auth_token,
            personal_token=None,
            oauth_config=None,
            ssl_verify=ssl_verify,
        )
    elif auth_type == "pat":
        return JiraConfig(
            url=jira_url,
            auth_type="pat",
            username=None,
            api_token=None,
            personal_token=auth_token,
            oauth_config=None,
            ssl_verify=ssl_verify,
        )
    elif auth_type == "oauth":
        # For OAuth, we create a minimal config with just the access token
        # The OAuth flow is already completed externally
        from mcp_atlassian.utils.oauth import BYOAccessTokenOAuthConfig

        # Extract cloud_id from URL if it's a Cloud instance
        cloud_id = None
        if "atlassian.net" in jira_url:
            # For Cloud instances, we'll need to derive cloud_id
            # This is a simplified approach - in production, you might need to call an API
            logger.debug(
                "Detected Atlassian Cloud URL. OAuth requires cloud_id which should be provided."
            )

        oauth_config = BYOAccessTokenOAuthConfig(
            access_token=auth_token,
            cloud_id=cloud_id or "",  # Will be handled by the fetcher
        )

        return JiraConfig(
            url=jira_url,
            auth_type="oauth",
            username=username,
            api_token=None,
            personal_token=None,
            oauth_config=oauth_config,
            ssl_verify=ssl_verify,
        )
    else:
        raise ValueError(
            f"Unsupported auth_type: {auth_type}. Must be 'oauth', 'pat', or 'basic'"
        )


def build_confluence_config_from_params(
    confluence_url: str,
    auth_token: str,
    auth_type: Literal["oauth", "pat", "basic"] = "oauth",
    username: str | None = None,
    ssl_verify: bool = True,
) -> ConfluenceConfig:
    """Build a ConfluenceConfig from function parameters.

    Args:
        confluence_url: Confluence instance URL (e.g., 'https://mycompany.atlassian.net/wiki')
        auth_token: Authentication token (OAuth token, PAT, or API token)
        auth_type: Authentication type ('oauth', 'pat', or 'basic')
        username: Username/email (required for 'basic' auth)
        ssl_verify: Whether to verify SSL certificates (default: True)

    Returns:
        ConfluenceConfig instance configured with the provided parameters

    Raises:
        ValueError: If required parameters are missing for the auth type
    """
    logger.debug(
        f"Building ConfluenceConfig from params: url={confluence_url}, auth_type={auth_type}, username={username}"
    )

    if auth_type == "basic":
        if not username:
            raise ValueError(
                "username is required for 'basic' authentication type"
            )
        return ConfluenceConfig(
            url=confluence_url,
            auth_type="basic",
            username=username,
            api_token=auth_token,
            personal_token=None,
            oauth_config=None,
            ssl_verify=ssl_verify,
        )
    elif auth_type == "pat":
        return ConfluenceConfig(
            url=confluence_url,
            auth_type="pat",
            username=None,
            api_token=None,
            personal_token=auth_token,
            oauth_config=None,
            ssl_verify=ssl_verify,
        )
    elif auth_type == "oauth":
        # For OAuth, we create a minimal config with just the access token
        from mcp_atlassian.utils.oauth import BYOAccessTokenOAuthConfig

        # Extract cloud_id from URL if it's a Cloud instance
        cloud_id = None
        if "atlassian.net" in confluence_url:
            logger.debug(
                "Detected Atlassian Cloud URL. OAuth requires cloud_id which should be provided."
            )

        oauth_config = BYOAccessTokenOAuthConfig(
            access_token=auth_token,
            cloud_id=cloud_id or "",
        )

        return ConfluenceConfig(
            url=confluence_url,
            auth_type="oauth",
            username=username,
            api_token=None,
            personal_token=None,
            oauth_config=oauth_config,
            ssl_verify=ssl_verify,
        )
    else:
        raise ValueError(
            f"Unsupported auth_type: {auth_type}. Must be 'oauth', 'pat', or 'basic'"
        )
