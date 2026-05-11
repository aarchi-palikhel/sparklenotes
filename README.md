# SparkleNotes ✨

A cute, feature-rich note-taking app with AI integration, email notifications, and a fully responsive design — built with Django and Tailwind CSS.

## Features

- **📝 Notes** — Create, edit, and organise your notes with a beautiful UI
- **✅ Todos** — Task management with due dates and AI-powered suggestions
- **🤖 Gemini AI** — Smart note summaries and todo suggestions via Google Gemini
- **📧 Email Integration** — Welcome emails on signup, forgot password flow, and overdue task reminders
- **🔐 Flexible Login** — Sign in with either your username or email address
- **👤 User Profiles** — Avatar upload (stored in DB), bio, and personal info
- **🛡️ Admin Tools** — Send overdue reminder emails to users directly from the admin panel
- **🌙 Dark Mode** — Toggle between light and dark themes
- **📱 Responsive** — Fully mobile-friendly with a slide-in sidebar

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.2 |
| Frontend | Tailwind CSS + Custom CSS |
| Database | PostgreSQL |
| AI | Google Gemini API |
| Email | Gmail SMTP (configurable) |

## Quick Start

See [SETUP.md](SETUP.md) for full installation instructions.

```bash
git clone https://github.com/aarchi-palikhel/sparklenotes.git
cd sparklenotes
pip install -r requirements.txt
cp .env.example .env   # fill in your credentials
python manage.py migrate
python manage.py runserver
```

## Project Structure

```
sparklenotes/
├── accounts/              # Auth, profiles, password reset
├── notes/                 # Notes, todos, AI features, admin tools
├── notes_project/         # Django project settings, Gemini client
├── templates/
│   ├── accounts/          # Login, register, profile, email templates
│   └── notes/             # Base layout, home, notes, todos
├── theme/                 # Tailwind CSS theme
├── .env.example           # Environment variable reference
└── requirements.txt
```

## Environment Variables

Copy `.env.example` to `.env` and fill in:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DB_NAME` / `DB_USER` / `DB_PASSWORD` | PostgreSQL credentials |
| `GEMINI_API_KEY` | Google Gemini API key |
| `EMAIL_HOST_USER` | Gmail address for sending emails |
| `EMAIL_HOST_PASSWORD` | Gmail App Password (16 chars, no spaces) |
| `SITE_URL` | Base URL used in email links (default: `http://127.0.0.1:8000`) |

## Admin — Overdue Reminders

Log in to `/admin/` and navigate to **Send Overdue Reminders** to send a single grouped email to every user who has incomplete todos past their due date. Each todo is only reminded once.

## Contributing

Feel free to fork and submit pull requests!
