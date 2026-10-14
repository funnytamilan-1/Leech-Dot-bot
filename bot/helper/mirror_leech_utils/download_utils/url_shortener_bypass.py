from ipaddress import ip_address
from re import search
from urllib.parse import urlparse

from curl_cffi import requests as cffi_requests

from ...ext_utils.exceptions import DirectDownloadLinkException

_OUO_DOMAINS = ("ouo.io", "ouo.press")

_CSRF_PATTERN = (
    r'<input[^>]*\bname="_token"[^>]*\bvalue="([^"]*)"'
    r'|<input[^>]*\bvalue="([^"]*)"[^>]*\bname="_token"'
)


def is_url_shortener(domain):
    host = (domain or "").lower().rstrip(".")
    if "://" in host:
        host = urlparse(host).hostname or ""
    return any(host == item or host.endswith("." + item) for item in _OUO_DOMAINS)


def _validate_redirect_target(location):
    """Reject unsafe or malformed redirect targets before passing them to downloaders."""
    try:
        parsed = urlparse(location)
        host = (parsed.hostname or "").lower().rstrip(".")
        if parsed.scheme not in ("http", "https") or not host:
            raise ValueError("redirect must be an absolute HTTP(S) URL")
        if parsed.username is not None or parsed.password is not None:
            raise ValueError("redirect URL must not contain credentials")
        if host == "localhost" or host.endswith((".localhost", ".local")):
            raise ValueError("redirect points to a local host")
        try:
            address = ip_address(host)
        except ValueError:
            address = None
        if address is not None and not address.is_global:
            raise ValueError("redirect points to a non-public IP address")
        return location
    except (TypeError, ValueError) as exc:
        raise DirectDownloadLinkException(f"ERROR: unsafe shortener redirect: {exc}") from None


def bypass_shortener(link):
    parsed = urlparse(link)
    domain = parsed.hostname or ""
    if parsed.scheme in ("http", "https") and is_url_shortener(domain):
        return _ouo(link)
    raise DirectDownloadLinkException(f"ERROR: No bypasser for {domain}")


def _extract_csrf(html):
    m = search(_CSRF_PATTERN, html)
    return next((g for g in m.groups() if g), "") if m else ""


def _ouo(link):
    """Resolve ouo.io / ouo.press shortlinks.

    Three-step CSRF dance: GET landing → POST /go/<id> → POST /xreallcygo/<id>.
    Cloudflare fronts ouo.io and fingerprints both TLS ClientHello and HTTP/2
    SETTINGS, so curl_cffi's chrome impersonation is required — stdlib
    requests/httpx gets 403.
    """
    parsed_input = urlparse(link)
    if parsed_input.scheme not in ("http", "https") or not is_url_shortener(parsed_input.hostname or ""):
        raise DirectDownloadLinkException("ERROR: unsupported or unsafe shortener URL")
    if (parsed_input.hostname or "").lower() == "ouo.press":
        normalized = parsed_input._replace(netloc=parsed_input.netloc.replace("ouo.press", "ouo.io")).geturl()
    else:
        normalized = link
    parsed = urlparse(normalized)
    short_id = parsed.path.rsplit("/", 1)[-1]
    if not short_id:
        raise DirectDownloadLinkException("ERROR: ouo: empty id segment")

    base = f"{parsed.scheme}://{parsed.netloc}"
    go_url = f"{base}/go/{short_id}"
    final_url = f"{base}/xreallcygo/{short_id}"

    try:
        with cffi_requests.Session(impersonate="chrome136", timeout=30) as s:
            r1 = s.get(normalized, allow_redirects=True)
            if r1.status_code == 403:
                raise DirectDownloadLinkException(
                    "ERROR: ouo.io blocked the request (403)"
                )
            tok1 = _extract_csrf(r1.text)
            if not tok1:
                raise DirectDownloadLinkException(
                    f"ERROR: ouo: _token not found on initial page (status={r1.status_code})"
                )

            r2 = s.post(
                go_url,
                data={"_token": tok1, "x-token": "", "v-token": "vm"},
                headers={"Origin": "https://ouo.io", "Referer": normalized},
                allow_redirects=False,
            )
            if r2.status_code == 403:
                raise DirectDownloadLinkException(
                    "ERROR: ouo.io blocked the request (403)"
                )
            if r2.status_code != 200:
                raise DirectDownloadLinkException(
                    f"ERROR: ouo: /go/ status {r2.status_code}"
                )
            tok2 = _extract_csrf(r2.text)
            if not tok2:
                raise DirectDownloadLinkException(
                    "ERROR: ouo: _token not found on /go/ page"
                )

            r3 = s.post(
                final_url,
                data={"_token": tok2, "x-token": ""},
                headers={"Origin": "https://ouo.io", "Referer": go_url},
                allow_redirects=False,
            )
            location = r3.headers.get("Location", "")
            if r3.status_code != 302 or not location:
                raise DirectDownloadLinkException(
                    f"ERROR: ouo: /xreallcygo/ status {r3.status_code} (location={location!r})"
                )
            return _validate_redirect_target(location)
    except DirectDownloadLinkException:
        raise
    except Exception as e:
        raise DirectDownloadLinkException(f"ERROR: ouo bypass failed: {e}") from e
