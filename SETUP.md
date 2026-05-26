# SparkleNotes: Setup Guide

## Prerequisites

- Python 3.10 or later — [python.org](https://www.python.org/downloads/)
- PostgreSQL 13 or later — [postgresql.org](https://www.postgresql.org/download/windows/)
- Node.js 18 or later — [nodejs.org](https://nodejs.org/) (required for Tailwind CSS)
- A Gmail account with 2-Step Verification enabled (required for email features)
- Git — [git-scm.com](https://git-scm.com/download/win)

---

## 1. Clone the repository

Open Command Prompt or PowerShell and run:

```powershell
git clone https://github.com/aarchi-palikhel/sparklenotes.git
cd sparklenotes
```

---

## 2. Create and activate a virtual environment

```powershell
python -m venv venv
venv\Scripts\activate
```

`(venv)` will be seen at the start of the prompt after activation.

---

## 3. Install Python dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Set up environment variables

```powershell
copy .env.example .env
```

Open `.env` in any text editor (Notepad, VS Code, etc.) and fill in all values:

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
EMAIL_HOST_PASSWORD=your16charapppassword
DEFAULT_FROM_EMAIL=SparkleNotes <your-email@gmail.com>

# Site URL (used in email links)
SITE_URL=http://127.0.0.1:8000
```

**Gmail App Password:**
1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Sign in and create a new app password (name it anything, e.g. SparkleNotes)
3. Copy the 16-character password and paste it into `EMAIL_HOST_PASSWORD`

**Development tip:** To print emails to the terminal instead of actually sending them, set:
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**Generate a Django secret key:**
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 5. Create the PostgreSQL database

Option A - using psql (Command Prompt):
```powershell
psql -U postgres -c "CREATE DATABASE notes_db;"
```

Option B - open pgAdmin, right-click Databases, and create a new database named `notes_db`.

---

## 6. Run migrations

```powershell
python manage.py migrate
```

---

## 7. Create a superuser

Required to access the admin panel at `/admin/`.

```powershell
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

---

## 8. Create the static folder

If it does not already exist:

```powershell
mkdir static
```

---

## 9. Set up Tailwind CSS

```powershell
python manage.py tailwind install
```

---

## 10. Start the development servers

Two separate terminal windows are needed, both with the virtual environment activated.

**Terminal 1 - Tailwind watcher:**
```powershell
python manage.py tailwind start
```

**Terminal 2 - Django development server:**
```powershell
python manage.py runserver
```

---

## 11. Open the app

- Application: http://127.0.0.1:8000
- Admin panel: http://127.0.0.1:8000/admin/

---

## Admin: Overdue Reminders

Log in to the admin panel with the superuser account. Click **Send Overdue Reminders** in the left sidebar. The page shows how many users have incomplete past-due todos and provides a single button to send grouped reminder emails. Each todo is only reminded once, the `reminder_sent` flag prevents duplicate emails.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `SMTPAuthenticationError` | Check `EMAIL_HOST_PASSWORD` — paste the app password without spaces |
| `column does not exist` | Run `python manage.py migrate` |
| `staticfiles.W004` | Run `mkdir static` in the project root |
| Tailwind styles not loading | Make sure `python manage.py tailwind start` is running in a separate terminal |
| Email not arriving | Check the spam folder; verify `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in `.env` |
| `psql` not recognised | Add PostgreSQL `bin` folder to your system PATH (e.g. `C:\Program Files\PostgreSQL\16\bin`) |
| `venv\Scripts\activate` fails | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` in PowerShell, then try again |
