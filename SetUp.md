# Set Up

## Spotify API App

- Create a [Spotify Application](https://developer.spotify.com/dashboard/applications)
- Take note of:
  - `Client ID`
  - `Client Secret`
- Click on **Edit Settings**
- In **Redirect URIs**:
  - Add `http://127.0.0.1:8888/callback`

> **Note:** Spotify no longer accepts `http://localhost/...` redirect URIs for
> new apps — you must use the explicit loopback IP `http://127.0.0.1` (with a
> port) or an HTTPS URL. If you followed an older guide using
> `http://localhost/callback/`, this is why it fails.

## Refresh Token

### Helper script (recommended)

From the root of this repo, run:

```sh
pip install requests
python3 get_refresh_token.py
```

It will ask for your Client ID and Client Secret, open your browser to
authorize, and print the `SPOTIFY_REFRESH_TOKEN` to copy into your deployment.

### Manual

- Navigate to the following URL (fill in your client ID):

```
https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&scope=user-read-currently-playing,user-read-recently-played,user-top-read&redirect_uri=http://127.0.0.1:8888/callback
```

- After logging in, your browser lands on an error page whose URL looks like
  `http://127.0.0.1:8888/callback?code={CODE}` — save the `{CODE}` portion.

- Create a string combining `{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}`
  (e.g. `5n7o4v5a3t7o5r2e3m1:5a8n7d3r4e2w5n8o2v3a7c5`) and **encode** it into
  [Base64](https://www.base64encode.org/).

- Then run a curl command in the form of:

```sh
curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -H "Authorization: Basic {BASE64}" -d "grant_type=authorization_code&redirect_uri=http://127.0.0.1:8888/callback&code={CODE}" https://accounts.spotify.com/api/token
```

- Save the `refresh_token` from the response

## Deployment

### Deploy to Vercel

- Register on [Vercel](https://vercel.com/)

- Fork this repo, then create a Vercel project linked to it

- Add Environment Variables:

  - `https://vercel.com/<YourName>/<ProjectName>/settings/environment-variables`
    - `SPOTIFY_REFRESH_TOKEN`
    - `SPOTIFY_CLIENT_ID`
    - `SPOTIFY_SECRET_ID`

- Deploy!

> If you deployed this project before and it stopped working, make sure your
> Vercel project is redeployed from the latest commit — old dependency pins
> (Flask 1.x) no longer run on Vercel's current Python runtime.

### Run locally with Docker

- You need to have [Docker](https://docs.docker.com/get-docker/) installed.

- Add Environment Variables to a `.env` file in the repo root:
  - `SPOTIFY_REFRESH_TOKEN`
  - `SPOTIFY_CLIENT_ID`
  - `SPOTIFY_SECRET_ID`
- To run the service, open a terminal in the root folder of the repo: <br>
  Execute:
  ```
  docker compose up
  ```
- When finished, navigate to [http://localhost:5000/](http://localhost:5000/)
- To stop the service, open a terminal in the root folder of the repo: <br>
  Execute:
  ```
  docker compose down
  ```

## ReadMe

You can now use the following in your readme (replace `<your-project>` with
your Vercel project domain):

`[![Spotify](https://<your-project>.vercel.app/api/spotify)](https://open.spotify.com/user/<your-spotify-username>)`

## Customization

### Hide the EQ bar

Uncomment the `contentBar = ""` line in the "not playing" branch of `makeSVG`
in [api/spotify.py](api/spotify.py), then the EQ bar will be hidden when
you're not currently playing anything.

### Status String

A string saying either "Vibing to:" (currently listening) or
"Recently played:" (not currently on Spotify) is shown by default. To hide
it, remove the `currentStatus` div in
[api/templates/spotify.html.j2](api/templates/spotify.html.j2) (or the dark
template) and reduce the card height in `api/spotify.py` (`cardHeight`).

### Theme Templates

If you want to change the widget theme, you can do so by changing the
`current-theme` property in [api/templates.json](api/templates.json).

Themes:

- `light`
- `dark`

If you wish to customize further, you can add your own customized
`spotify.html.j2` file to the templates folder, and add the theme and file
name to the `templates` dictionary in the `templates.json` file.

### Top tracks panel

By default the badge shows an "On repeat lately" panel next to the player with
your most-played tracks of roughly the last 4 weeks (Spotify's finest
granularity).

- Requires the `user-top-read` scope on your refresh token. If your token was
  generated without it, the panel is hidden automatically and only the player
  is shown — re-run `get_refresh_token.py` and update
  `SPOTIFY_REFRESH_TOKEN` to enable it.
- `top_tracks` URL param controls the number of tracks (0–5).
  `?top_tracks=0` hides the panel and restores the compact player-only card.

### Color

You can customize the appearance of your `Card` however you wish with URL
params:

- `background_color` - Card's background color _(hex color)_ without `#`
- `border_color` - Card border color _(hex color)_ without `#`
- `top_tracks` - Number of top tracks in the side panel (0-5, default 5)

Example: `/api/spotify?background_color=0d1117&border_color=ffffff&top_tracks=5`

### Spotify Logo

You can add the Spotify logo by un-commenting the `spotify-logo` block near
the bottom of the template file.

## Debugging

If the badge shows a broken image on GitHub, open your badge URL
(`https://<your-project>.vercel.app/api/spotify`) directly in a browser first.

- **500 error / `KeyError`** — usually a wrong or expired
  `SPOTIFY_REFRESH_TOKEN`, or a mismatched `SPOTIFY_CLIENT_ID` /
  `SPOTIFY_SECRET_ID`. Re-run `get_refresh_token.py` and update the env vars,
  then redeploy.
- **Build fails on Vercel** — make sure you're deploying the latest commit of
  this repo (modern `requirements.txt`).
- **Check the function logs** in Vercel under your project's
  **Deployments → Functions** tab; most issues show up there as missing or
  invalid credentials.
