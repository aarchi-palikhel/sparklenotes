# SparkleNotes — Setup Guide

## Prerequisites

- Python 3.10+
- PostgreSQL 13+
- Node.js 18+ (for Tailwind CSS)
- A Gmail account with 2-Step Verification enabled (for email features)

---

## 1. Clone the repository

```bash
git clone https://github.com/aarchi-palikhel/sparklenotes.git
cd sparklenotes
```

## 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

## 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

## 4. Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in all values:

```env
# Django
SECRET_KEY=your-secret-key-here

# PostgreSQL
DB_NAME=notes_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Google Gemini AI
GEMINI_API_KEY=your-gemini-api-key

# Email (Gmail SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
DEFAULT_FROM_EMAIL=SparkleNotes <your-email@gmail.com>

# Site URL (used in email links)
SITE_URL=http://127.0.0.1:8000
```

> **Gmail App Password:** Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords), create an app password, and paste it **without spaces** into `EMAIL_HOST_PASSWORD`. Requires 2-Step Verification to be enabled.

> **Development tip:** To print emails to the terminal instead of sending them, set:
> ```env
> EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
> ```

## 5. Create the PostgreSQL database

```bash
# Using psql
psql -U postgres -c "CREATE DATABASE notes_db;"
```

Or create it via pgAdmin.

## 6. Run migrations

```bash
python manage.py migrate
```

## 7. Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```

## 8. Set up Tailwind CSS

```bash
python manage.py tailwind install
```

## 9. Start the development servers

Open **two terminals**:

```bash
# Terminal 1 — Tailwind watcher
python manage.py tailwind start

# Terminal 2 — Django dev server
python manage.py runserver
```

## 10. Open the app

- App: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Getting API Keys

### Google Gemini AI
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Click **Get API key** → Create a new key
3. Paste it into `GEMINI_API_KEY` in your `.env`

### Django Secret Key
Generate a secure key with:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Admin — Overdue Reminders

Log in to `/admin/` with your superuser account and click **Send Overdue Reminders** in the sidebar. The dashboard shows how many users have overdue incomplete todos and lets you send grouped reminder emails with one click.

Each todo is only reminded **once** — the `reminder_sent` flag prevents duplicate emails.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `SMTPAuthenticationError` | Check your Gmail App Password — paste it without spaces |
| `column does not exist` | Run `python manage.py migrate` |
| `staticfiles.W004` | The `static/` folder is missing — create it with `mkdir static` |
| Tailwind styles not loading | Run `python manage.py tailwind start` in a separate terminal |
| Email not arriving | Check spam folder; verify `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in `.env` |
