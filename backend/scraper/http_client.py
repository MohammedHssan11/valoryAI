import json
import random
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .config import DEFAULT_HEADERS, ScraperConfig


class NonJSONResponseError(RuntimeError):
    """Raised when server returns HTML/challenge instead of JSON."""


class RequestFailedError(RuntimeError):
    """Raised when we fail after retries."""


@dataclass
class HttpResult:
    status_code: int
    url: str
    json_data: Dict[str, Any]


class PropertyFinderHTTPClient:
    def __init__(self, cfg: Optional[ScraperConfig] = None, headers: Optional[Dict[str, str]] = None):
        self.cfg = cfg or ScraperConfig()
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        if headers:
            self.session.headers.update(headers)

    def build_url(self) -> str:
        return urljoin(self.cfg.base_url, self.cfg.endpoint)

    def _sleep_backoff(self, attempt: int) -> None:
        # Exponential backoff with jitter
        base = self.cfg.backoff_base_s * (2 ** (attempt - 1))
        sleep_s = base + random.uniform(0, self.cfg.jitter_s)
        time.sleep(sleep_s)

    def get_json(self, params: Dict[str, Any]) -> HttpResult:
        url = self.build_url()
        last_err: Optional[Exception] = None

        for attempt in range(1, self.cfg.max_retries + 1):
            try:
                resp = self.session.get(url, params=params, timeout=self.cfg.timeout_s)

                # Retryable status codes
                if resp.status_code in (429, 500, 502, 503, 504):
                    last_err = RequestFailedError(f"Retryable HTTP {resp.status_code}")
                    self._sleep_backoff(attempt)
                    continue

                # Hard fail for common blocks/forbidden
                if resp.status_code in (401, 403):
                    # Often WAF / forbidden. Could be token/cookie needed.
                    raise RequestFailedError(
                        f"Blocked or unauthorized (HTTP {resp.status_code}). "
                        f"Response snippet: {resp.text[:200]}"
                    )

                # Try parse JSON safely
                content_type = (resp.headers.get("Content-Type") or "").lower()
                text_head = resp.text[:200].lstrip()

                # If content type isn't json OR it starts with '<' => likely HTML/WAF page
                if ("application/json" not in content_type) or text_head.startswith("<"):
                    raise NonJSONResponseError(
                        f"Expected JSON but got Content-Type='{content_type}'. "
                        f"Snippet: {resp.text[:200]}"
                    )

                try:
                    data = resp.json()
                except json.JSONDecodeError as e:
                    raise NonJSONResponseError(f"JSON decode failed: {e}. Snippet: {resp.text[:200]}")

                return HttpResult(status_code=resp.status_code, url=resp.url, json_data=data)

            except (requests.Timeout, requests.ConnectionError) as e:
                last_err = e
                self._sleep_backoff(attempt)
                continue
            except (NonJSONResponseError, RequestFailedError) as e:
                # For these, we still may retry a couple times (sometimes transient)
                last_err = e
                if attempt < self.cfg.max_retries:
                    self._sleep_backoff(attempt)
                    continue
                break
            except Exception as e:
                last_err = e
                break

        raise RequestFailedError(f"Failed after {self.cfg.max_retries} attempts. Last error: {last_err}")
