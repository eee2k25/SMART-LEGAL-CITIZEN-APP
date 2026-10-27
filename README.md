# Smart Legal & Citizen Support Platform

A Django monolith for public legal-information discovery, complaint preparation, public-service discovery, advocate directory browsing, and a retrieval-based information assistant. This workspace contains a runnable academic demonstration build, not a law firm or government service.

## Project overview

Citizens often need to navigate information distributed across legal sources, public-service pages, grievance portals, and professional directories. CivicLaw provides a single responsive interface to search a curated library, open cited public sources, prepare a checklist, and find the relevant next step.

### Objectives and scope

- Present general, jurisdiction-labelled legal and citizen-service information.
- Search the published library and directory records.
- Support accounts, saved articles, and saved checklists.
- Direct users to official sources without claiming to submit anything.
- Keep the core assistant usable without a paid model API.

**Important:** This platform is not a substitute for a qualified lawyer, an official authority, or emergency services. No legal filing, advocate contact, or government case update is performed here. Content needs ongoing human review.

## Features

- Responsive homepage, navigation, legal library, category/search, detail pages and source references.
- Advocate directory with name/practice/location search and admin-controlled verification status. Demo profiles are fictional and labelled.
- Complaint guides and user-specific saved checklist progress.
- Citizen-services directory with official-site links.
- Emergency section citing India ERSS 112 (`https://112.gov.in/`).
- User registration, login/logout, password reset, profile, password change, dashboard, bookmarks, and account deletion.
- Retrieval-based assistant matching question terms against published article fields; it is explicitly not generative AI.
- Feedback storage and administrator moderation through Django admin.
- Django admin content management and server-side permissions.
- SQLite local database; PostgreSQL URL support for production; WhiteNoise static files; Render configuration.
- Fifteen automated tests (see `docs/TESTING.md`).

## Roles

- **Visitor:** public pages, search, and registration.
- **Citizen:** own profile, bookmarks, checklist progress, feedback, assistant access, and own account deletion.
- **Administrator:** Django staff/superuser permissions control admin content, feedback moderation, and advocate verification. Ordinary users cannot promote themselves.

Advocate login/profile management and inquiry delivery are not implemented. No known administrator credentials are created by seed data.

## Technology and architecture

Python 3.11+ recommended (tested here with Python 3.13.16), Django 5.2, Django Templates, HTML/CSS/JavaScript, SQLite, optional PostgreSQL via `DATABASE_URL`, Gunicorn and WhiteNoise. Applications are kept deliberately simple: one `support` app owns the related models and views; Django's built-in auth/admin provide authentication and content moderation.

```text
config/       Django project settings and routing
support/      Models, forms, views, URLs, admin, tests, seed command
 templates/   Shared layout, public pages, account templates
static/css/   Responsive accessible stylesheet
docs/         Architecture, data, security, testing, deployment, user guide, report
```

Detailed diagrams and data model notes: `docs/ARCHITECTURE.md`, `docs/DATABASE.md`.

## Local setup

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env and set a development-only SECRET_KEY.
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py test
python manage.py runserver
```

If PowerShell script activation is restricted, do not weaken system-wide execution policy. Run `.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.venv\Scripts\python.exe manage.py ...` directly.

### macOS / Linux

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env; use a local development-only SECRET_KEY.
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py test
python manage.py runserver
```

The project uses Django's default username-based login. The registration form requires a unique email and validates passwords with Django's validators. Passwords are hashed by Django. Local password-reset links print to the development server console; this does **not** send an email.

### Local URLs

- Home: http://127.0.0.1:8000/
- Login: http://127.0.0.1:8000/account/login/
- Registration: http://127.0.0.1:8000/register/
- Dashboard (login required): http://127.0.0.1:8000/dashboard/
- Admin: http://127.0.0.1:8000/admin/
- Legal library/search: http://127.0.0.1:8000/legal/
- Advocate directory: http://127.0.0.1:8000/advocates/
- Complaint guidance: http://127.0.0.1:8000/complaints/
- Citizen services: http://127.0.0.1:8000/services/
- Assistant: http://127.0.0.1:8000/assistant/

Run `python manage.py seed_demo` again safely to refresh the supplied demonstration records. It creates no administrator. Create one separately with `python manage.py createsuperuser`.

## Configuration and deployment

See `docs/DEPLOYMENT.md` and `render.yaml`. Locally, SQLite is selected by default. In production, set a PostgreSQL `DATABASE_URL`; the settings parser configures Django's PostgreSQL backend and requires TLS by default. Set a unique long `SECRET_KEY`, `DEBUG=False`, correct `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and `SECURE_SSL_REDIRECT=True`. Production cookies are secure and HSTS is enabled when `DEBUG=False`. `build.sh` installs requirements, collects static files, and runs migrations. Configure a real email backend before relying on password-reset delivery; console email is the default and is not delivery.

Never commit `.env`, database dumps, production credentials, user data, or API keys.

## Tests

```bash
python manage.py test
python manage.py check
```

Detailed test scope and actual run results are in `docs/TESTING.md`. Tests cover public/draft visibility, registration and password hashing, duplicate email rejection, authentication gating, user-owned bookmarks, feedback persistence, assistant search, and checklist record scope.

## Security and privacy

CSRF middleware, Django authentication/password hashing, server-side authorization, ORM parameterization, HTML autoescaping, safe external-link attributes, session HTTP-only cookies, secure production cookies, password-reset tokens, and minimal profile collection are in place. User-owned bookmarks/checklists are queried by authenticated user; account deletion cascades to those records. Feedback stays for review without its user relation after deletion. See `docs/SECURITY.md`.

No conversation history is stored. Do not submit sensitive case facts to feedback or assistant. There is no external LLM, advocate contact service, upload handling, or complaint filing integration. Login rate limiting is not installed in this build; deploy behind a managed WAF/rate limiter before public launch.

## Known limitations

- No original project review guide was present in the initial workspace, so no guide-specific technology constraints could be confirmed.
- Legal demo entries and service links are starter content, not a professional legal review. Admins should verify all sources, jurisdiction, currency, and wording before public use.
- Directory demo profiles are explicitly fictional. There are no real advocate profiles or credential checks.
- Assistant is deterministic database keyword retrieval, not an LLM and not legal advice.
- No full interface translation; content fields allow language labels, interface is English.
- No advocate registration workflow, appointment messaging, in-app notifications, activity log, or audit log beyond Django's built-in admin log.
- Account deletion immediately deletes account and saved items; feedback is retained without a user link. No formal retention policy/legal hold workflow is implemented.
- Production deployment was prepared but not performed or verified from this workspace.

## Further project documentation

- `docs/ARCHITECTURE.md`
- `docs/DATABASE.md`
- `docs/SECURITY.md`
- `docs/TESTING.md`
- `docs/DEPLOYMENT.md`
- `docs/USER_GUIDE.md`
- `docs/PROJECT_REPORT.md`
