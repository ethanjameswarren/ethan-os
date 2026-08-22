#!/usr/bin/env python3
"""
One-time Spotify authorization for EJ OS (Authorization Code flow).

Run this once per machine, after creating a Spotify developer app (see
docs/domains/music/spotify-setup.md). It opens the Spotify consent screen, catches the redirect
on a local loopback server, exchanges the authorization code for tokens, and prints the refresh
token for you to store as the SPOTIFY_REFRESH_TOKEN environment variable.

The refresh token is never written to a file by this script -- it is printed once to your
terminal so you can add it to your own environment/secret manager, the same way NOTION_TOKEN is
managed for the ethan-notion scripts.

Usage:
  python auth.py

Environment (required):
  SPOTIFY_CLIENT_ID
  SPOTIFY_CLIENT_SECRET

Redirect URI: register exactly this in your Spotify app settings (HTTPS/loopback-IP only, per
Spotify's current requirements -- plain "localhost" is no longer accepted):
  http://127.0.0.1:8888/callback
"""

import base64
import json
import os
import secrets
import sys
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPES = "playlist-modify-private playlist-read-private"


class CallbackHandler(BaseHTTPRequestHandler):
    result = {}

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        CallbackHandler.result["code"] = params.get("code", [None])[0]
        CallbackHandler.result["state"] = params.get("state", [None])[0]
        CallbackHandler.result["error"] = params.get("error", [None])[0]
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(
            b"<html><body><h2>EJ OS Spotify authorization complete.</h2>"
            b"You can close this tab and return to the terminal.</body></html>"
        )

    def log_message(self, *args):  # silence default request logging
        pass


def main():
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise SystemExit(
            "Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET before running this script. "
            "See docs/domains/music/spotify-setup.md."
        )

    state = secrets.token_urlsafe(16)
    auth_params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "state": state,
    }
    auth_url = f"{AUTHORIZE_URL}?{urllib.parse.urlencode(auth_params)}"

    print("Opening Spotify authorization in your browser...")
    print(f"If it doesn't open automatically, visit:\n  {auth_url}\n")
    webbrowser.open(auth_url)

    server = HTTPServer(("127.0.0.1", 8888), CallbackHandler)
    print("Waiting for Spotify to redirect back to http://127.0.0.1:8888/callback ...")
    server.handle_request()  # blocks for exactly one request

    result = CallbackHandler.result
    if result.get("error"):
        raise SystemExit(f"Spotify authorization failed: {result['error']}")
    if result.get("state") != state:
        raise SystemExit("State mismatch -- possible interception. Aborting; please retry.")
    code = result.get("code")
    if not code:
        raise SystemExit("No authorization code received. Please retry.")

    token_body = urllib.parse.urlencode(
        {"grant_type": "authorization_code", "code": code, "redirect_uri": REDIRECT_URI}
    ).encode("utf-8")
    req = urllib.request.Request(TOKEN_URL, data=token_body, method="POST")
    basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode("ascii")
    req.add_header("Authorization", f"Basic {basic}")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Token exchange failed ({e.code}): {e.read().decode()}") from e

    refresh_token = payload.get("refresh_token")
    if not refresh_token:
        raise SystemExit("No refresh_token in the response -- unexpected. Please retry.")

    print("\nAuthorization successful.\n")
    print("Set this as a persistent environment variable (do not commit it anywhere):\n")
    print(f"  SPOTIFY_REFRESH_TOKEN={refresh_token}\n")
    print(
        "Once SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, and SPOTIFY_REFRESH_TOKEN are all set in "
        "your environment, normal EJ OS Spotify workflows will refresh access tokens "
        "automatically -- you should not need to run this again unless you revoke access or "
        "change Spotify apps."
    )


if __name__ == "__main__":
    main()
