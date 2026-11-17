# CampusLore

CampusLore is a Reddit-style anonymous Q&A platform for JIIT students. Visitors can browse questions and answers, but only authenticated students with a valid `@mail.jiit.ac.in` email can create questions, answer, vote, confirm, or report content.

## Project overview

- Anonymous posting using generated JIITIAN-style display names
- Google OAuth login restricted to college email domains
- Mandatory profile completion for branch and year
- Public question listing, search, and dashboard
- Question and answer voting with reputation tracking
- Reporting and moderation workflow
- CSV and PDF export for superusers
- Hardcoded JIIT college data and programs page

## Tech stack

- Python 3
- Django 4.x
- django-allauth
- SQLite (for development)
- ReportLab for PDF export
- Bootstrap for the first-pass UI

## Local setup

### 1) Open the project folder

```bash
cd CampusLore
```

### 2) Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Apply the database schema and seed demo data

```bash
python manage.py migrate
python manage.py seed_data
```

### 5) Create an admin user (optional but recommended)

```bash
python manage.py createsuperuser
```

### 6) Start the Django server

```bash
python manage.py runserver
```

Then open:

- Home: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

---

## Google authentication setup

To allow Google sign-in, create OAuth credentials in Google Cloud Console.

### Step 1: Create a Google Cloud project

1. Go to https://console.cloud.google.com/
2. Create a new project or select an existing one.
3. Enable the Google Identity / OAuth APIs for your project.

### Step 2: Create OAuth client ID

1. Open "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Web application"
4. Add the redirect URI:

```text
http://127.0.0.1:8000/accounts/google/login/callback/
```

### Step 3: Add environment values

```bash
export GOOGLE_CLIENT_ID="your-google-client-id"
export GOOGLE_CLIENT_SECRET="your-google-client-secret"
```

### Step 4: Run the app again

```bash
python manage.py runserver
```

---

## Authentication rules

- Only email addresses ending in `@mail.jiit.ac.in` are allowed to sign in.
- Guests can read public content.
- Login is required for creating questions, answering, voting, confirming, and reporting.
- First-time users are redirected to the profile completion page to enter branch and year.

## Important files

- `campuslore/settings.py` – Django project settings and allauth setup
- `core/adapters.py` – email-domain restriction logic
- `core/models.py` – user, question, answer, vote, report, and program models
- `core/management/commands/seed_data.py` – starter data for categories and programs
- `core/college_data.py` – hardcoded JIIT information
- `README.md` – setup and authentication guide

## Admin and moderation

Superusers can:

- view admin statistics dashboard
- export CSV reports
- export PDF reports
- review user reports from the Django admin interface

## Notes

- All project files are kept inside the CampusLore workspace.
- Google OAuth requires valid credentials from the Google Cloud Console.
- The project is designed for college-only access and anonymous community participation.

---

## Summary

CampusLore is a campus-focused social Q&A platform that gives JIIT students a safe way to ask and answer questions anonymously while staying restricted to the college community. It demonstrates Django authentication, database modeling, moderation, anonymous community interactions, and admin reporting in a single practical project.
