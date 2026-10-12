"""Shortener integrations used by Leech Dot Bot.

Made by @Code_Dots · Partner: @CodeRips
Keep provider credentials in private runtime configuration; never log API keys.
"""

import asyncio
import base64
import random
from urllib.parse import quote

from cloudscraper import create_scraper

try:
    from urllib3 import disable_warnings
except ImportError:
    def disable_warnings(*args, **kwargs):
        """Compatibility fallback for older urllib3 installations."""


from ... import LOGGER, shortener_dict
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


def _short_url_sync(longurl):
    """Synchronous provider adapter; called through asyncio.to_thread."""
    disable_warnings()

    if Config.PROTECTED_API:
        response = _request("GET", Config.PROTECTED_API, params={"url": longurl})
        payload = response.json()
        if payload.get("status") == "success" and payload.get("url"):
            return payload["url"]
        raise ValueError("Protected shortener API returned an unsuccessful response")

    if not shortener_dict:
        return longurl

    shortener, api_key = random.choice(list(shortener_dict.items()))
    if "shorte.st" in shortener:
        response = _request(
            "PUT",
            "https://api.shorte.st/v1/data/url",
            headers={"public-api-token": api_key},
            data={"urlToShorten": longurl},
        )
        result = response.json().get("shortenedUrl")
    elif "linkvertise" in shortener:
        encoded = quote(base64.b64encode(longurl.encode("utf-8")).decode("ascii"), safe="")
        hosts = ("link-to.net", "up-to-down.net", "direct-link.net", "file-link.net")
        host = random.choice(hosts)
        result = f"https://{host}/{api_key}/{random.random() * 1000:.6f}/dynamic?r={encoded}"
    elif "bitly.com" in shortener:
        response = _request(
            "POST",
            "https://api-ssl.bit.ly/v4/shorten",
            json={"long_url": longurl},
            headers={"Authorization": f"Bearer {api_key}"},
        )
        result = response.json().get("link")
    elif "ouo.io" in shortener:
        response = _request("GET", f"https://ouo.io/api/{api_key}", params={"s": longurl})
        result = response.text.strip()
    elif "cutt.ly" in shortener:
        response = _request(
            "GET",
            "https://cutt.ly/api/api.php",
            params={"key": api_key, "short": longurl},
        )
        result = response.json().get("url", {}).get("shortLink")
    else:
        response = _request(
            "GET",
            f"https://{shortener}/api",
            params={"api": api_key, "url": longurl},
        )
        result = response.json().get("shortenedUrl")

    if isinstance(result, str) and result.startswith(("https://", "http://")):
        return result
    raise ValueError(f"Shortener provider '{shortener}' returned no valid URL")


async def short_url(longurl, attempt=0):
    """Shorten a URL without blocking the bot's asyncio event loop.

    If all configured providers fail, return the original URL so a temporary
    shortener outage does not make unrelated bot commands unresponsive.
    """
    if not shortener_dict and not Config.PROTECTED_API:
        return longurl

    tries = max(0, _MAX_ATTEMPTS - int(attempt or 0))
    for retry in range(tries):
        try:
            return await asyncio.to_thread(_short_url_sync, longurl)
        except Exception as exc:
            # Do not log request URLs or provider payloads: they can contain
            # user-specific deep links and credentials.
            LOGGER.warning(
                "Shortener request failed (attempt %s/%s): %s",
                retry + 1,
                tries,
                type(exc).__name__,
            )
            if retry + 1 < tries:
                await asyncio.sleep(min(0.5 * (2**retry), 4))
    return longurl
