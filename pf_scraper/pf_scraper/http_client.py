# pf_scraper/http_client.py
from __future__ import annotations

import json
import random
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

import requests

from .config import DEFAULT_HEADERS, ScraperConfig


class RequestFailedError(RuntimeError):
    pass


class NextDataNotFoundError(RuntimeError):
    pass


@dataclass
class HttpResult:
    status_code: int
    url: str
    json_data: Dict[str, Any]
    final_content_type: str
    text_snippet: str = ""


class PropertyFinderHTTPClient:
    """
    Unified HTTP client for PropertyFinder (UAE/EG):
    - Fetch SSR HTML
    - Extract __NEXT_DATA__ JSON
    - Retries + backoff
    - Supports passing either relative path or full URL
    """

    def __init__(
        self,
        cfg: Optional[ScraperConfig] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.cfg = cfg or ScraperConfig()
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        if headers:
            self.session.headers.update(headers)

    # -------------------------
    # internal helpers
    # -------------------------
    def _sleep(self, attempt: int, base: float = 0.6) -> None:
        jitter = random.uniform(0, 0.35)
        time.sleep(base * (2 ** max(0, attempt - 1)) + jitter)

    def _normalize_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        - drop None
        - keep lists/tuples (doseq)
        - cast scalars to str
        """
        out: Dict[str, Any] = {}
        for k, v in (params or {}).items():
            if v is None:
                continue
            if isinstance(v, (list, tuple)):
                out[k] = [str(x) for x in v if x is not None]
            else:
                out[k] = str(v)
        return out

    def _merge_query(self, url: str, params: Dict[str, Any]) -> str:
        if not params:
            return url

        u = urlparse(url)
        qs = parse_qs(u.query, keep_blank_values=True)

        for k, v in params.items():
            if isinstance(v, (list, tuple)):
                qs[k] = [str(x) for x in v]
            else:
                qs[k] = [str(v)]

        new_query = urlencode(qs, doseq=True)
        return urlunparse((u.scheme, u.netloc, u.path, u.params, new_query, u.fragment))

    def build_url(self, path_or_url: str, params: Optional[Dict[str, Any]] = None) -> str:
        params = self._normalize_params(params or {})

        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            return self._merge_query(path_or_url, params)

        base = self.cfg.base_url.rstrip("/")
        path = path_or_url if path_or_url.startswith("/") else f"/{path_or_url}"
        url = f"{base}{path}"
        if params:
            return f"{url}?{urlencode(params, doseq=True)}"
        return url

    def _extract_next_data(self, html: str) -> Dict[str, Any]:
        """
        Safer extractor:
        - find the script tag containing id="__NEXT_DATA__"
        - slice from '>' to '</script>'
        """
        marker = 'id="__NEXT_DATA__"'
        i = html.find(marker)
        if i == -1:
            raise NextDataNotFoundError("Could not find __NEXT_DATA__ marker in HTML.")

        # go backwards to find "<script"
        s = html.rfind("<script", 0, i)
        if s == -1:
            raise NextDataNotFoundError("Could not locate <script ...> for __NEXT_DATA__ marker.")

        # find '>' end of script open tag
        j = html.find(">", i)
        if j == -1:
            raise NextDataNotFoundError("Malformed __NEXT_DATA__ script tag (no '>').")

        # closing script
        k = html.find("</script>", j)
        if k == -1:
            raise NextDataNotFoundError("Malformed __NEXT_DATA__ script tag (no </script>).")

        raw = html[j + 1 : k].strip()
        if not raw:
            raise NextDataNotFoundError("__NEXT_DATA__ script content is empty.")

        try:
            data = json.loads(raw)
        except Exception as e:
            raise NextDataNotFoundError(f"Failed to parse __NEXT_DATA__ JSON: {e}")

        if not isinstance(data, dict):
            raise NextDataNotFoundError(f"__NEXT_DATA__ is not an object (type={type(data)}).")
        return data

    def _request_html(self, url: str) -> Tuple[requests.Response, str]:
        resp = self.session.get(url, timeout=self.cfg.timeout_s, allow_redirects=True)
        ct = (resp.headers.get("Content-Type") or "").lower()
        return resp, ct

    def _is_retryable_status(self, code: int) -> bool:
        return code in (408, 425, 429, 500, 502, 503, 504)

    # -------------------------
    # public APIs
    # -------------------------
    def get_json(self, path: str, params: Optional[Dict[str, Any]] = None) -> HttpResult:
        params = params or {}
        last_err: Optional[Exception] = None

        for attempt in range(1, self.cfg.max_retries + 1):
            try:
                url = self.build_url(path, params)
                resp, ct = self._request_html(url)

                if self._is_retryable_status(resp.status_code):
                    last_err = RequestFailedError(f"Retryable HTTP {resp.status_code}")
                    self._sleep(attempt, base=0.8)
                    continue

                if resp.status_code in (401, 403):
                    snippet = (resp.text or "")[:250]
                    raise RequestFailedError(f"Blocked (HTTP {resp.status_code}). URL: {resp.url}. Snippet: {snippet}")

                resp.raise_for_status()

                data = self._extract_next_data(resp.text)

                time.sleep(random.uniform(0.25, 0.65))

                return HttpResult(
                    status_code=resp.status_code,
                    url=resp.url,
                    json_data=data,
                    final_content_type=ct,
                    text_snippet=(resp.text or "")[:180],
                )

            except (requests.Timeout, requests.ConnectionError) as e:
                last_err = e
                self._sleep(attempt, base=0.8)
                continue
            except (NextDataNotFoundError, RequestFailedError) as e:
                last_err = e
                if attempt < self.cfg.max_retries:
                    self._sleep(attempt, base=0.9)
                    continue
                break
            except Exception as e:
                last_err = e
                break

        raise RequestFailedError(f"Failed after {self.cfg.max_retries} attempts. Last error: {last_err}")

    def get_raw(self, url: str) -> requests.Response:
        last_err: Optional[Exception] = None

        for attempt in range(1, self.cfg.max_retries + 1):
            try:
                resp = self.session.get(url, timeout=self.cfg.timeout_s, allow_redirects=True)

                if self._is_retryable_status(resp.status_code):
                    last_err = RequestFailedError(f"Retryable HTTP {resp.status_code} on raw page")
                    self._sleep(attempt, base=0.8)
                    continue

                if resp.status_code in (401, 403):
                    snippet = (resp.text or "")[:250]
                    raise RequestFailedError(f"Blocked (HTTP {resp.status_code}) on raw page. Snippet: {snippet}")

                resp.raise_for_status()
                return resp

            except (requests.Timeout, requests.ConnectionError) as e:
                last_err = e
                self._sleep(attempt, base=0.8)
                continue
            except Exception as e:
                last_err = e
                if attempt < self.cfg.max_retries:
                    self._sleep(attempt, base=0.9)
                    continue
                break

        raise RequestFailedError(f"Raw fetch failed after {self.cfg.max_retries} attempts. Last error: {last_err}")
