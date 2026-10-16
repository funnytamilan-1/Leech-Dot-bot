"""Shortener integrations used by Leech Dot Bot.

Made by @Code_Dots · Partner: @CodeRips
Keep provider credentials in private runtime configuration; never log API keys.
"""

import asyncio
from urllib.parse import urlsplit

from cloudscraper import create_scraper

try:
    from urllib3 import disable_warnings
except ImportError:
    def disable_warnings(*args, **kwargs):
        """Compatibility fallback for older urllib3 installations."""


from ... import LOGGER
from ...core.config_manager import Config

_REQUEST_TIMEOUT = 20
_MAX_ATTEMPTS = 4


def _request(method, url, **kwargs):
    """Run one bounded HTTP request and reject HTTP error responses."""
    kwargs.setdefault("timeout", _REQUEST_TIMEOUT)
    scraper = create_scraper()
    try:
        response = scraper.request(method, url, **kwargs)
        response.raise_for_status()
        return response
    finally:
        scraper.close()


def _validated_short_url(value):
    """Accept only absolute HTTPS links from shortener providers."""
    if not isinstance(value, str):
        return None
    value = value.strip()
    try:
        parsed = urlsplit(value)
    except ValueError:
        return None
    if parsed.scheme != "https" or not parsed.hostname:
        return None
    return value


def _response_json_or_short_url(response, provider_name):
    """Parse JSON APIs, while supporting providers that return a plain URL."""
    try:
        return response.json()
    except ValueError as exc:
        raw = (response.text or "").strip()
        plain_url = _validated_short_url(raw)
        if plain_url:
            return plain_url
        content_type = (response.headers.get("Content-Type") or "unknown").split(";", 1)[0]
        raise ValueError(
            f"{provider_name} returned non-JSON data "
            f"(HTTP {response.status_code}, content-type={content_type})"
        ) from exc


def _short_url_sync(longurl):
    """Synchronous provider adapter; called through asyncio.to_thread."""
    disable_warnings()

    custom_api_url = (Config.get("SHORTENER_API_URL") or "").strip()
    custom_api_key = (Config.get("SHORTENER_API_KEY") or "").strip()
    if custom_api_url:
        parsed_endpoint = urlsplit(custom_api_url)
        if parsed_endpoint.scheme != "https" or not parsed_endpoint.hostname:
            raise ValueError("Custom shortener API endpoint must use HTTPS")
        if not custom_api_key:
            raise ValueError("Custom shortener API key is not configured")
        method = (Config.get("SHORTENER_API_METHOD") or "GET").strip().upper()
        if method not in ("GET", "POST"):
            raise ValueError("Custom shortener method must be GET or POST")
        key_param = (Config.get("SHORTENER_API_KEY_PARAM") or "api").strip()
        url_param = (Config.get("SHORTENER_URL_PARAM") or "url").strip()
        response_field = (Config.get("SHORTENER_RESPONSE_FIELD") or "shortenedUrl").strip()
        if not key_param or not url_param or not response_field:
            raise ValueError("Custom shortener parameter/response fields cannot be empty")
        request_data = {key_param: custom_api_key, url_param: longurl}
        response = _request(
            method,
            custom_api_url,
            params=request_data if method == "GET" else None,
            json=request_data if method == "POST" else None,
        )
        payload = _response_json_or_short_url(response, "Custom shortener API")
        if isinstance(payload, str):
            result = _validated_short_url(payload)
        else:
            result = payload
            for field in response_field.split("."):
                if not isinstance(result, dict):
                    result = None
                    break
                result = result.get(field)
            result = _validated_short_url(result)
        if result:
            return result
        raise ValueError("Custom shortener API returned no valid HTTPS URL")

    raise ValueError("No custom shortener API is configured")

async def short_url(longurl, attempt=0):
    """Shorten a URL without blocking the bot's asyncio event loop.

    If the advanced API is not configured, return the original URL. When
    verification is enabled, the caller detects this and does not unlock access.
    """
    if not Config.shortener_provider_configured():
        return longurl

    tries = max(0, _MAX_ATTEMPTS - int(attempt or 0))
    for retry in range(tries):
        try:
            return await asyncio.to_thread(_short_url_sync, longurl)
        except Exception as exc:
            # Do not log request URLs or provider payloads: they can contain
            # user-specific deep links and credentials.
            # ValueError messages in this module are deliberately sanitized (status/content type
            # or validation hints). Other exception text may contain request URLs or credentials.
            safe_detail = str(exc)[:180] if isinstance(exc, ValueError) else type(exc).__name__
            LOGGER.warning(
                "Shortener request failed (attempt %s/%s): %s",
                retry + 1,
                tries,
                safe_detail,
            )
            if retry + 1 < tries:
                await asyncio.sleep(min(0.5 * (2**retry), 4))
    return longurl
