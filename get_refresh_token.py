#!/usr/bin/env python3
"""Interactive helper to obtain the SPOTIFY_REFRESH_TOKEN for this badge.

Prerequisite: in your Spotify app settings (https://developer.spotify.com/dashboard),
add exactly this Redirect URI:

    http://127.0.0.1:8888/callback

Then run:  python3 get_refresh_token.py
"""
import base64
import http.server
import urllib.parse
import webbrowser

import requests

REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "user-read-currently-playing user-read-recently-played"


def main():
    client_id = input("Spotify Client ID: ").strip()
    client_secret = input("Spotify Client Secret: ").strip()

    auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode({
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
    })

    code_holder = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if "code" in params:
                code_holder["code"] = params["code"][0]
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Done! Close this tab and return to the terminal.")
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, *args):
            pass

    server = http.server.HTTPServer(("127.0.0.1", 8888), Handler)
    print("\nOpening your browser to authorize with Spotify...")
    print(f"If nothing opens, visit this URL manually:\n\n{auth_url}\n")
    webbrowser.open(auth_url)
    while "code" not in code_holder:
        server.handle_request()
    server.server_close()

    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code_holder["code"],
            "redirect_uri": REDIRECT_URI,
        },
        headers={"Authorization": f"Basic {auth}"},
        timeout=10,
    ).json()

    if "refresh_token" not in response:
        raise SystemExit(f"Token exchange failed: {response}")

    print("\nAdd this environment variable to your deployment:\n")
    print(f"SPOTIFY_REFRESH_TOKEN={response['refresh_token']}")


if __name__ == "__main__":
    main()
