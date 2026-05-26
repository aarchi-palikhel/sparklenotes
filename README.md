# SparkleNotes

A full-stack note-taking and task management web application built with Django and Tailwind CSS. It includes AI-powered writing tools, automated email notifications, user authentication, and a fully responsive interface.

---

## Features

### Notes and Tasks
- Create, edit, delete, and organise personal notes
- Task management with optional due dates and completion tracking
- Notes and todos are scoped per user, no cross-user data access

### AI Integration (Google Gemini)
- Summarise any note with one click
- Rewrite a note to be clearer or more formal
- Auto-suggest a title based on note content
- Detect the emotional tone of a note
- Suggest a realistic due date based on task description
- AI-powered subtask suggestions for todos
- Weekly digest page with a personalised AI summary of the past 7 days

### Email
- Welcome email sent automatically on registration
- Forgot password flow with a time-limited reset link
- Overdue task reminder emails sent from the admin panel (one grouped email per user, sent once per todo)

### Authentication
- Register and log in with username or email address
- Password reset via email
- User profiles with avatar (stored in the database), bio, and personal info

### Admin
- Custom admin dashboard for sending overdue reminder emails
- User notes and todos are not visible in the admin — only aggregate counts are shown

### UI and Accessibility
- Light and dark mode toggle, persisted in localStorage
- Fully responsive layout with a fixed sidebar on desktop and a slide-in drawer on mobile
- Password visibility toggle on all password fields
- Auto-dismissing notifications with a manual close button

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.2 |
| Frontend | Tailwind CSS, Custom CSS |
| Database | PostgreSQL |
| AI | Google Gemini API (`google-generativeai`) |
| Email | SMTP (Gmail by default, configurable) |
| Auth | Django built-in authentication |

---

## Project Structure

```
sparklenotes/
├── accounts/                  # Registration, login, profiles, password reset
├── notes/                     # Notes, todos, AI views, admin tools
├── notes_project/             # Django settings, URLs, Gemini client
├── templates/
│   ├── accounts/              # Auth pages and email templates
│   └── notes/                 # Base layout, home, notes, todos, digest
├── theme/                     # Tailwind CSS configuration
├── static/                    # Static assets (favicon, etc.)
├── .env.example               # Environment variable reference
├── requirements.txt
├── README.md
└── SETUP.md
```


## Admin: Overdue Reminders

Log in to `/admin/` with a superuser account and open **Send Overdue Reminders** from the sidebar. The dashboard shows how many users have incomplete past-due todos and lets you send grouped reminder emails with a single button click. Each todo is flagged after being reminded so duplicate emails are never sent.

---

## AI Fallback

If the Gemini API quota is exceeded or unavailable, the application automatically falls back to pre-written responses. Users always receive a result, the app never crashes or shows an error due to AI unavailability.

---

## Contributing

Fork the repository and open a pull request. Please create a feature branch rather than committing directly to `main`.
