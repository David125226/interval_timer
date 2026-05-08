# Interval Timer

A browser-based interval timer for group fitness sessions, with timers stored in PostgreSQL so they're available on any device.

## Run locally

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Set the database URL (requires a local or remote PostgreSQL instance):
   ```
   $env:DATABASE_URL = "postgresql://user:password@localhost/interval_timer"
   ```
3. Start the server:
   ```
   python app.py
   ```
4. Open `http://localhost:8000`

## Deploy to Railway

### First time

1. Push this folder to a GitHub repository.
2. Go to [railway.app](https://railway.app) and create a new project → **Deploy from GitHub repo**.
3. In the project, click **+ New** → **Database** → **Add PostgreSQL**. Railway sets `DATABASE_URL` automatically.
4. Railway detects the `Procfile` and deploys automatically. Your public URL appears in the **Settings** tab.

### Subsequent deploys

Push to GitHub — Railway redeploys automatically.

## Features

- Configurable work/rest intervals with named exercises
- Round and session repeat controls
- Fullscreen display with colour-coded timer (red = work, green = rest)
- Audible bell on phase transitions
- Timers saved to PostgreSQL — accessible from any device
