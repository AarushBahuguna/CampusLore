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
cd /home/aarushb/Documents/CampusLore
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

To allow Google sign-in, you must create OAuth credentials in Google Cloud Console.

### Step 1: Create a Google Cloud project

1. Go to https://console.cloud.google.com/
2. Create a new project or select an existing one.
3. Enable the Google Identity / OAuth APIs for your project.

### Step 2: Create OAuth client ID

1. Open "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Web application"
4. Add your authorized redirect URI:

```text
http://127.0.0.1:8000/accounts/google/login/callback/
```

If you deploy later, add your production domain too, for example:

```text
https://your-domain.com/accounts/google/login/callback/
```

### Step 3: Add the values to your environment

In your terminal, set:

```bash
export GOOGLE_CLIENT_ID="your-google-client-id"
export GOOGLE_CLIENT_SECRET="your-google-client-secret"
```

You can also add these to a `.env` file if you want to manage them outside the shell, but this project is configured to read the environment variables directly from Django settings.

### Step 4: Run the app again

```bash
python manage.py runserver
```

Then click the Sign In button in the app and choose Google.

---

## Authentication rules

- Only email addresses ending in `@mail.jiit.ac.in` are allowed to sign in.
- Guests can read the public pages and browse the content.
- Log in is required for creating questions, answering, voting, confirming, and reporting.
- First-time users are redirected to the profile completion page to enter their branch and year.

## Important files

- `campuslore/settings.py` – Django project settings and allauth configuration
- `core/adapters.py` – email-domain restriction logic
- `core/models.py` – user, question, answer, vote, report, and program models
- `core/management/commands/seed_data.py` – starter category/program data
- `college_details.txt` – source data for JIIT details
- `README.md` – setup and authentication documentation

## Admin and moderation

Superusers can:

- view the admin statistics dashboard
- export CSV reports
- export PDF reports
- review user reports from the Django admin interface

## Notes

- All project files are kept inside the CampusLore workspace.
- Batch size information for programs is intentionally left as a placeholder to be updated later.
- Google OAuth needs valid credentials from the Google Cloud Console for live login to work.

## Authentication rules

- Only email addresses ending in `@mail.jiit.ac.in` are allowed to sign in.
- Unauthenticated users can read public content.
- Engagement actions require login.
- New users are redirected to a profile completion page to fill in branch and year.

## Important files

- `campuslore/settings.py` – Django project settings and allauth configuration
- `core/models.py` – application models
- `core/views.py` – public, authenticated, and admin views
- `core/adapters.py` – email domain restriction logic
- `core/college_data.py` – hardcoded JIIT information
- `college_details.txt` – source data used to populate the JIIT college information
- `core/management/commands/seed_data.py` – startup data seeding

## Admin and moderation

Superusers can:

- view the admin statistics dashboard
- export CSV reports
- export PDF reports
- review user reports from the Django admin interface

## Notes

- All project files are kept inside the CampusLore workspace.
- Batch size information for programs is intentionally left as placeholder data that can be updated later.
- Google OAuth requires valid credentials from the Google Cloud Console.
