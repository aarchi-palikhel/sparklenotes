# SparkleNotes Setup Guide

## Prerequisites
- Python 3.8+
- PostgreSQL (optional - SQLite used by default)
- Node.js (for Tailwind CSS)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aarchi-palikhel/sparklenotes.git
   cd sparklenotes
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # On Mac/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file with your settings:
   ```env
   SECRET_KEY=your-super-secret-key-here
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

5. **Set up Tailwind CSS**
   ```bash
   cd theme
   npm install
   cd ..
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development servers**
   ```bash
   # Terminal 1 - Tailwind
   python manage.py tailwind start

   # Terminal 2 - Django
   python manage.py runserver
   ```

9. **Visit the app**
   Open http://127.0.0.1:8000

## Getting API Keys

### Gemini AI API
1. Go to [Google AI Studio]
2. Create a new API key
3. Add it to your `.env` file

### Generate Django Secret Key
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

