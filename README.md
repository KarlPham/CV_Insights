
#   CV Insights – Final Deployment Guide

This document provides final instructions on how to deploy the **Dockerized version** of the CV Insights project. This includes setting up credentials, configuring the environment, and running the app using Docker.

---

## 📦 What Is Dockerized?

| Component     | Docker Service | Description |
|---------------|----------------|-------------|
| Streamlit App | `app`          | Hosts the resume analysis frontend and handles all Gemini + OAuth logic |
| PostgreSQL DB | `db`           | Stores users, resumes, job descriptions, match scores, and skill suggestions |

---

## 🌱 Docker Branch

The `Docker` branch is dedicated to Docker support. Clone it using:

```bash
git clone https://github.com/your-org/cv-insights.git
cd cv-insights
git checkout Docker
```

---

## 🗂️ Project Structure

⬜ ![](/Users/imouli/Documents/Screenshot 2025-05-26 at 12.11.50 PM.png)

Key files:
- `Dockerfile` – builds the app container
- `docker-compose.yml` – runs both app and DB containers
- `.dockerignore` – excludes temp folders and secrets
- `.streamlit/secrets.toml` – **used to store all app secrets**
- `.env` – only for Docker database container

---

## 🔐 Credentials Setup

### ✅ `.streamlit/secrets.toml` (App-level config)

Create this file manually inside `.streamlit/`. It is **not version-controlled**.

```toml
[google]
api_key = "your_google_gemini_api_key"

[connections.postgres]
type = "sql"
dialect = "postgresql"
host = "db"
port = 5432
database = "cv_insights"
username = "postgres"
password = "your password"

[oauth]
client_id = "your_google_oauth_client_id"
client_secret = "your_google_oauth_client_secret"
```

> 📌 Streamlit automatically reads this file inside Docker. You do **not** need to pass these as environment variables.

---

### ✅ `.env` (Docker database setup only)

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=cv_insights
```

> ⚠️ This is only used for the `db` service inside `docker-compose.yml`.

---

## ⚠️ PostgreSQL Port Usage Note

Docker binds PostgreSQL to port `5432` by default:

```yaml
ports:
  - "5432:5432"
```

If this port is **already in use** on your local machine:

- Change to another host-side port like `5433`:

```yaml
ports:
  - "5433:5432"
```

- ✅ You **do not** need to change anything in `secrets.toml` since Streamlit accesses the DB internally over port `5432`.

---

## 🧪 Run Locally with Docker

```bash
docker-compose up --build
```

To stop:

```bash
docker-compose down
```

To remove volumes and reset the DB:

```bash
docker-compose down -v
```

---

## 📝 OAuth & Gemini Notes

- Each user who clones this repo must:
  - Create their own **Google Gemini API key**
  - Register their own **OAuth credentials** via [Google Cloud Console](https://console.cloud.google.com/)
  - Fill out their own `secrets.toml`

---


