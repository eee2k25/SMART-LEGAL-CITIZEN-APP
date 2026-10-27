# Start here in VS Code

This archive contains the Django project source. It intentionally excludes the development database, secrets, virtual environments, and generated static files. You will create a fresh local database by running migrations.

## 1. Extract and open

1. Extract `Smart-Legal-Citizen-Support.zip` to a folder you can write to.
2. In VS Code, choose **File → Open Folder…** and select the extracted `Smart-Legal-Citizen-Support` folder.
3. Open **Terminal → New Terminal**. Ensure the terminal is at the project root (the folder containing `manage.py`).
4. Use Python 3.11 or newer.

## 2. Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` in VS Code and change `SECRET_KEY` to a long, random development-only value. You can generate one with:

```powershell
py -c "import secrets; print(secrets.token_urlsafe(48))"
```

Paste the generated value after `SECRET_KEY=` in `.env`. Then run:

```powershell
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py seed_demo
.venv\Scripts\python.exe manage.py createsuperuser
.venv\Scripts\python.exe manage.py test
.venv\Scripts\python.exe manage.py runserver
```

If PowerShell blocks virtual-environment activation, the commands above deliberately call the environment's Python directly; you do not need to weaken the machine's execution policy.

## 3. macOS or Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
python3 -c 'import secrets; print(secrets.token_urlsafe(48))'
```

Paste the generated value into `.env` after `SECRET_KEY=`. Then run:

```bash
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_demo
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py test
.venv/bin/python manage.py runserver
```

## 4. Open the website

- Home: http://127.0.0.1:8000/
- Register: http://127.0.0.1:8000/register/
- Log in: http://127.0.0.1:8000/account/login/
- Admin: http://127.0.0.1:8000/admin/
- Legal information: http://127.0.0.1:8000/legal/
- Advocates: http://127.0.0.1:8000/advocates/
- Complaint guides: http://127.0.0.1:8000/complaints/
- Citizen services: http://127.0.0.1:8000/services/

Keep the terminal running while using the site. Press **Ctrl+C** there to stop it. The admin account is the one you created with `createsuperuser`; the demo-data command creates no administrator.

## Important

The app uses SQLite locally and prints password-reset emails to the development terminal; it does not send real email until you configure an email provider. Demo advocate entries are fictional. Legal text is general demonstration content and needs qualified review before public use. Do not submit sensitive legal case information.

For architecture, security, tests, and deployment guidance, see `README.md` and the `docs/` folder.
