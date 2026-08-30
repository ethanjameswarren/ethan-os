#!/usr/bin/env python3
"""
One-time Google Calendar authorization for Ethan OS (Authorization Code flow).

Run this once per machine, after creating a Google Cloud OAuth client
(see docs/integrations/google-calendar.md). It opens the Google consent screen,
catches the redirect on a local loopback server, exchanges the authorization code
for tokens, and prints the refresh token for you to store as the
GOOGLE_REFRESH_TOKEN environment variable.

The refresh token is never written to a file by this script.

Usage:
  python auth.py

Environment (required):
  GOOGLE_CLIENT_ID
  GOOGLE_CLIENT_SECRET

Redirect URI: register exactly this in your Google Cloud credentials:
  http://127.0.0.1:8888/callback
"""

import json
import os
import secrets
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
READONLY_SCOPE = "https://www.googleapis.com/auth/calendar.readonly"
EVENTS_SCOPE = "https://www.googleapis.com/auth/calendar.events"
SCOPES = f"{READONLY_SCOPE} {EVENTS_SCOPE}"


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
            b"<html><body><h2>Google Calendar authorization complete.</h2>"
            b"You can close this tab and return to the terminal.</body></html>"
        )

    def log_message(self, *args):
        pass


def main():
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise SystemExit(
            "Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET before running this script. "
            "See docs/integrations/google-calendar.md."
        )

    state = secrets.token_urlsafe(16)
    auth_params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "state": state,
        "access_type": "offline",
        "prompt": "consent",
    }
    auth_url = f"{AUTHORIZE_URL}?{urllib.parse.urlencode(auth_params)}"

    print("Opening Google Calendar authorization in your browser...")
    print(f"If it doesn't open automatically, visit:\n  {auth_url}\n")
    webbrowser.open(auth_url)

    server = HTTPServer(("127.0.0.1", 8888), CallbackHandler)
    print("Waiting for Google to redirect back to http://127.0.0.1:8888/callback ...")
    server.handle_request()

    result = CallbackHandler.result
    if result.get("error"):
        raise SystemExit(f"Google authorization failed: {result['error']}")
    if result.get("state") != state:
        raise SystemExit("State mismatch -- possible interception. Aborting; please retry.")
    code = result.get("code")
    if not code:
        raise SystemExit("No authorization code received. Please retry.")

    token_body = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode("utf-8")
    req = urllib.request.Request(TOKEN_URL, data=token_body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Token exchange failed ({e.code}): {e.read().decode()}") from e

    refresh_token = payload.get("refresh_token")
    if not refresh_token:
        raise SystemExit(
            "No refresh_token in the response. "
            "Make sure you set access_type=offline and prompt=consent. Please retry."
        )

    print("\nAuthorization successful.\n")
    print("Set this as a persistent environment variable (do not commit it anywhere):\n")
    print(f"  GOOGLE_REFRESH_TOKEN={refresh_token}\n")
    print(
        "Once GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_REFRESH_TOKEN are all set, "
        "Ethan OS will refresh short-lived access tokens automatically. "
        "Re-run this script only if you revoke access or switch Google Cloud projects."
    )


if __name__ == "__main__":
    main()
