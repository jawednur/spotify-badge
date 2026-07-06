# Spotify "Now Playing" badge

A live badge for your GitHub profile README showing the song you're currently
listening to on Spotify (or, when nothing is playing, a recently played track).

It works as a tiny Flask app deployed as a Vercel serverless function: every
time someone views your profile, GitHub fetches
`https://<your-project>.vercel.app/api/spotify`, which asks the Spotify API
what's playing and renders it as an animated SVG.

## Setup

Follow [SetUp.md](SetUp.md). Short version:

1. Create a [Spotify app](https://developer.spotify.com/dashboard) and add
   `http://127.0.0.1:8888/callback` as a Redirect URI.
2. Run `python3 get_refresh_token.py` to get your `SPOTIFY_REFRESH_TOKEN`.
3. Import this repo into [Vercel](https://vercel.com/new) and set the
   environment variables `SPOTIFY_CLIENT_ID`, `SPOTIFY_SECRET_ID`, and
   `SPOTIFY_REFRESH_TOKEN`, then deploy.
4. Add the badge to your profile README (replace `<your-project>` with your
   Vercel project domain):

```markdown
[![Spotify](https://<your-project>.vercel.app/api/spotify?background_color=0d1117&border_color=ffffff)](https://open.spotify.com/user/<your-spotify-username>)
```

## Customization

Options are set with URL parameters:

- `background_color` — card background (hex without `#`)
- `border_color` — card border (hex without `#`)
- `top_tracks` — number of tracks in the "On repeat lately" side panel
  (0–5, default 5; requires a refresh token with the `user-top-read` scope,
  otherwise the panel hides itself)

The badge also shows a status line: "Vibing to:" when you're listening right
now, "Recently played:" when you're not.

See [SetUp.md](SetUp.md#customization) for themes and more options.

## Credits

Based on [novatorem/novatorem](https://github.com/novatorem/novatorem)
(unlicensed).
