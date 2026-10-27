# Deployment (Render reference path)

Deployment is prepared, **not performed to a public host**. The deployment security check `python manage.py check --deploy` passed using a simulated production environment (DEBUG=False, example host/origin and a non-production test secret); this does not verify provider networking, email, or a public instance. `render.yaml` defines a Django web service and PostgreSQL database; hosting plans, names, and pricing are provider-controlled and may need adjustment.

## Deploy using the blueprint

1. Push this project to a private or public GitHub repository.
2. In Render, create a Blueprint from that repository and review the `render.yaml` resource plan before applying it.
3. Render provisions the web service and PostgreSQL database, injects a generated `SECRET_KEY`, database connection string and the example canonical host. If Render assigns another host, update both `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` to the actual hostname/origin.
4. Build command: `./build.sh` (pip install, collectstatic, migrate). Start command: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 60`.
5. Confirm `DEBUG=False`, database `DATABASE_URL`, allowed host and trusted origin. Never paste credentials in Git.
6. After deploy, use Render Shell or a one-off job to run `python manage.py seed_demo` if the demonstration catalog is wanted. Create a staff account with `python manage.py createsuperuser` in a secure one-off shell; do not seed an admin.
7. Configure real SMTP (`EMAIL_BACKEND` should be Django SMTP backend plus `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL`). Password reset cannot deliver while console backend is configured.
8. Visit the generated URL, test `/`, `/legal/`, `/advocates/`, `/complaints/`, `/services/`, `/account/login/`, `/admin/`; verify CSS, HTTPS redirects, reset-email delivery, and database persistence.

## Production configuration

`DATABASE_URL` supports PostgreSQL connection strings. TLS is requested through `DB_SSLMODE=require`. WhiteNoise compressed static manifest storage serves collected files. Set `ALLOWED_HOSTS` as comma-separated hostnames (no scheme); `CSRF_TRUSTED_ORIGINS` uses full origins including `https://`. `SECURE_SSL_REDIRECT` defaults to true in production. HTTPS proxy header support is configured for common managed hosts.

Run `python manage.py check --deploy` against the actual host environment. Run migrations using the release command or `python manage.py migrate --noinput`; do not run concurrent migrations from multiple workers. Set up database backups and test restoration. SQLite on an ephemeral web container is not recommended for production.

## Troubleshooting

- **400 DisallowedHost:** add the exact deployed hostname to `ALLOWED_HOSTS`.
- **CSRF 403 after deploy:** add exact `https://host` to `CSRF_TRUSTED_ORIGINS` and confirm the host sends the forwarded HTTPS header.
- **Missing static files:** verify `collectstatic` ran successfully and `STATIC_ROOT` is populated.
- **Postgres connection error:** validate `DATABASE_URL`, SSL requirements and network access; make sure `psycopg` is installed.
- **Reset message absent:** console backend logs the email only to application logs; configure a real provider and verify it.
- **Seed changes not present:** run `python manage.py seed_demo` as a one-off task.

No public deployment URL is available because deployment credentials and an external project/repository account were not supplied.
