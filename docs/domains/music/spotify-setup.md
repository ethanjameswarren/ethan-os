# Spotify integration — one-time setup

This is the only manual setup Ethan needs to do. After this, normal use (export/sync/resolve/
review) refreshes access tokens automatically.

## 1. Create a Spotify developer app

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and log in
   with your Spotify account.
2. Create a new app (any name/description, e.g. "EJ OS").
3. Note the **Client ID** and **Client Secret** from the app's settings.

## 2. Configure the redirect URI

In the app's settings, add this exact redirect URI:

```
http://127.0.0.1:8888/callback
```

Spotify no longer accepts a plain `localhost` redirect URI (only HTTPS or a loopback IP address
like `127.0.0.1`), so this must be the literal IP form above.

## 3. Provide credentials via environment variables

Set these in your shell/environment (never commit them to any repository):

```
SPOTIFY_CLIENT_ID=<your client id>
SPOTIFY_CLIENT_SECRET=<your client secret>
```

## 4. Authorize EJ OS once

From `ethan-os/scripts/spotify/`, run:

```
python auth.py
```

This opens the Spotify consent screen in your browser, catches the redirect locally, and prints a
`SPOTIFY_REFRESH_TOKEN` value. Add that to your environment the same way as the two values above:

```
SPOTIFY_REFRESH_TOKEN=<printed value>
```

## 5. Normal use

With all three environment variables set, every Spotify workflow (`export-dj-set-to-spotify`,
`sync-dj-set-to-spotify`, `resolve-spotify-track`, `review-spotify-matches`) refreshes short-lived
access tokens automatically — you should never need to touch a token directly again unless you
revoke access in your Spotify account or switch developer apps, in which case just re-run
`auth.py`.

## Scopes requested

`playlist-modify-private playlist-read-private` — only enough to create/modify Ethan's own private
playlists and verify they still exist. No read access to listening history, top tracks, follows,
or public-profile playlist publishing is requested.

## Known Spotify platform limitation: playlist privacy

Verified live against the current Spotify Web API (2026-08): EJ OS requests `public: false` when
creating a playlist, but Spotify's API currently reports the playlist as public (`public: true`)
immediately afterward regardless. This matches long-standing community reports that the Web API's
public/private flag is unreliable, not a bug in EJ OS's request. Until Spotify fixes this,
if you want a set's playlist to actually be private, set it to private manually from the Spotify
app after EJ OS creates it (playlist menu → "Make secret"/"Make private").

## What EJ OS never does with your Spotify account

- Never makes a playlist public without being asked.
- Never reads or stores your listening history, saved tracks, or other library data.
- Never treats a manual edit you make in the Spotify app as a canonical change to a DJ set.
- Never writes Spotify-derived data (genre tags, popularity, audio features) into your DJ/AI
  assessment data.
