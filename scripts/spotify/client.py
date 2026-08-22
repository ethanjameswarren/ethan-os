#!/usr/bin/env python3
"""
Minimal Spotify Web API client shared by scripts/spotify/*.py.

No third-party dependencies (matches the ethan-notion scripts' convention of stdlib + PyYAML
only). Uses the Authorization Code flow: EJ OS runs locally as a long-running personal tool that
can safely hold a client secret in the environment (same trust model as NOTION_TOKEN), so this is
a confidential client per Spotify's own guidance -- PKCE is for clients that *can't* store a
secret, which doesn't apply here.

Secrets (read from the environment only; never written to disk or logged):
  SPOTIFY_CLIENT_ID
  SPOTIFY_CLIENT_SECRET
  SPOTIFY_REFRESH_TOKEN  (obtained once via auth.py)

Scopes requested by auth.py: playlist-modify-private playlist-read-private
"""

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE = "https://api.spotify.com/v1"

SCOPES = "playlist-modify-private playlist-read-private"


class SpotifyAuthError(RuntimeError):
    """Raised when credentials are missing or the refresh token is invalid/revoked."""


class SpotifyAPIError(RuntimeError):
    def __init__(self, status, message):
        super().__init__(f"Spotify API error {status}: {message}")
        self.status = status


def _require_env(name):
    value = os.environ.get(name)
    if not value:
        raise SpotifyAuthError(
            f"{name} is not set. Run scripts/spotify/auth.py once to complete Spotify setup "
            "(see docs/domains/music/spotify-setup.md)."
        )
    return value


def get_access_token():
    """Exchange the long-lived refresh token for a short-lived access token. Called once per
    script invocation; never persisted to disk."""
    client_id = _require_env("SPOTIFY_CLIENT_ID")
    client_secret = _require_env("SPOTIFY_CLIENT_SECRET")
    refresh_token = _require_env("SPOTIFY_REFRESH_TOKEN")

    body = urllib.parse.urlencode(
        {"grant_type": "refresh_token", "refresh_token": refresh_token}
    ).encode("utf-8")
    req = urllib.request.Request(TOKEN_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    basic = _basic_auth_header(client_id, client_secret)
    req.add_header("Authorization", f"Basic {basic}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        text = e.read().decode()
        raise SpotifyAuthError(
            f"Refresh token exchange failed ({e.code}): {text}. The refresh token may have been "
            "revoked -- re-run scripts/spotify/auth.py."
        ) from e
    return payload["access_token"]


def _basic_auth_header(client_id, client_secret):
    import base64

    raw = f"{client_id}:{client_secret}".encode("utf-8")
    return base64.b64encode(raw).decode("ascii")


def request(method, path, token, params=None, json_body=None, retries=3):
    """Call the Spotify Web API, handling rate limiting (429) and one 401 retry after a fresh
    token fetch. `path` is relative to API_BASE (e.g. "/search")."""
    url = f"{API_BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    body = json.dumps(json_body).encode("utf-8") if json_body is not None else None
    attempt = 0
    while True:
        attempt += 1
        req = urllib.request.Request(url, data=body, method=method)
        req.add_header("Authorization", f"Bearer {token}")
        if body is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                text = resp.read().decode()
                return json.loads(text) if text else None
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt <= retries:
                retry_after = int(e.headers.get("Retry-After", "1"))
                time.sleep(retry_after)
                continue
            if e.code == 401 and attempt <= 1:
                token = get_access_token()
                continue
            text = e.read().decode()
            raise SpotifyAPIError(e.code, text) from e


def search_track(token, query, limit=10, market=None):
    params = {"q": query, "type": "track", "limit": limit}
    if market:
        params["market"] = market
    resp = request("GET", "/search", token, params=params)
    return resp.get("tracks", {}).get("items", [])


def get_current_user_id(token):
    resp = request("GET", "/me", token)
    return resp["id"]


def create_playlist(token, user_id, name, description, public=False):
    """Creates a playlist for the currently-authenticated user via POST /me/playlists.

    `user_id` is accepted for backward compatibility with callers but is unused: the older
    POST /users/{user_id}/playlists endpoint is being restricted for apps registered after
    Spotify's Nov 2024 API changes and returns 403 for this app; /me/playlists is the current,
    non-deprecated endpoint and always targets the token's own user.

    KNOWN SPOTIFY PLATFORM LIMITATION (observed live, 2026-08): passing public=False is honored in
    this call's own response, but a subsequent GET on the playlist reports public=True regardless.
    This matches long-standing community reports that the Web API's public/private flag on
    playlist creation is unreliable. EJ OS still requests public=False (harmless, and correct if
    Spotify fixes this), but do not rely on it for real privacy -- see
    docs/domains/music/spotify-setup.md for the current workaround (set it to private manually in
    the Spotify app after creation).
    """
    return request(
        "POST",
        "/me/playlists",
        token,
        json_body={"name": name, "description": description, "public": public},
    )


def get_playlist(token, playlist_id):
    try:
        return request("GET", f"/playlists/{playlist_id}", token)
    except SpotifyAPIError as e:
        if e.status == 404:
            return None
        raise


def replace_playlist_items(token, playlist_id, uris):
    """Full idempotent replace, chunked to Spotify's 100-URI-per-request limit.

    Uses /playlists/{id}/items (not the older /playlists/{id}/tracks, removed in Spotify's
    February 2026 Web API changes -- see docs/domains/music/spotify-setup.md).
    """
    first, rest = uris[:100], uris[100:]
    request("PUT", f"/playlists/{playlist_id}/items", token, json_body={"uris": first})
    for i in range(0, len(rest), 100):
        chunk = rest[i : i + 100]
        request("POST", f"/playlists/{playlist_id}/items", token, json_body={"uris": chunk})


def get_playlist_items(token, playlist_id):
    """Return the set of track URIs currently in a playlist (paginated). Uses the current
    /playlists/{id}/items endpoint; each entry's track/episode object is under the "item" key
    (renamed from "track" in Spotify's February 2026 Web API changes)."""
    uris = set()
    endpoint = f"/playlists/{playlist_id}/items"
    params = {"limit": 100, "offset": 0}
    while True:
        resp = request("GET", endpoint, token, params=params)
        for entry in resp.get("items", []):
            item = entry.get("item")
            if item and item.get("uri"):
                uris.add(item["uri"])
        if not resp.get("next"):
            break
        params["offset"] += 100
    return uris


def add_playlist_items(token, playlist_id, uris):
    """Purely additive: appends URIs not already checked, never replaces/removes existing items.
    Chunked to Spotify's 100-URI-per-request limit."""
    for i in range(0, len(uris), 100):
        chunk = uris[i : i + 100]
        request("POST", f"/playlists/{playlist_id}/items", token, json_body={"uris": chunk})


def update_playlist_details(token, playlist_id, name=None, description=None):
    body = {}
    if name is not None:
        body["name"] = name
    if description is not None:
        body["description"] = description
    if body:
        request("PUT", f"/playlists/{playlist_id}", token, json_body=body)
