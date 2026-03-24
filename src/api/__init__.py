"""
API 包导出
"""
from src.api.serpapi import serpapi_client, google_client, SerpAPIClient, GoogleSearchClient
from src.api.firecrawl import firecrawl_client, FirecrawlClient
from src.api.duckduckgo import duckduckgo_client, DuckDuckGoSearchClient

__all__ = [
    "serpapi_client",
    "google_client",
    "firecrawl_client",
    "duckduckgo_client",
    "SerpAPIClient",
    "GoogleSearchClient",
    "FirecrawlClient",
    "DuckDuckGoSearchClient"
]