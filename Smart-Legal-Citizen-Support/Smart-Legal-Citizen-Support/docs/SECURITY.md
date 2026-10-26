# Security notes

## Implemented controls

- Django CSRF middleware and CSRF tokens on POST forms, including logout and destructive account deletion.
- Django authentication and password hashing/password validators; password reset uses Django's token flow.
- `login_required` on dashboards, saved data, assistant session entry, bookmarks, checklist updates, profile and account deletion.
- Staff-only Django admin with model-specific permissions; advocate status is changed via admin, not a citizen-facing form.
- Django ORM rather than interpolated SQL; Django template autoescaping.
- Search strings are length-limited; public queries constrain published records.
- Session and CSRF cookies are HTTP-only. When `DEBUG=False`, HTTPS redirect, secure cookies and HSTS are configured.
- `SECRET_KEY` and database URL come from environment; `.env` is ignored; no admin password is seeded.
- Minimal profile fields; assistant conversations are not persisted; no sensitive file uploads.
- External links use `rel="noopener noreferrer"` when opened in new tabs.

## Deployment checklist

1. Generate a unique secret (e.g. `python -c "import secrets; print(secrets.token_urlsafe(64))"`) and set `SECRET_KEY` in the host.
2. Set `DEBUG=False`, exact `ALLOWED_HOSTS`, exact HTTPS `CSRF_TRUSTED_ORIGINS`, PostgreSQL `DATABASE_URL`, and TLS.
3. Configure SMTP or a transactional email service for password reset; test delivery and SPF/DKIM separately.
4. Add edge rate limiting / WAF for login, registration and feedback; this build does not implement per-IP login throttling.
5. Configure backups, monitor errors, rotate credentials, and restrict database network access.
6. Run `python manage.py check --deploy`; warnings that depend on the host's proxy/HTTPS configuration must be checked in that deployment environment.
7. Arrange legal-content review, privacy review and incident response before public launch.

## Known security gaps

No rate-limiting middleware, CAPTCHA, explicit consent-version record, formal audit-log UI, email verification, or professional content review workflow exists. Django admin's built-in log is available but is not a comprehensive security audit log. Do not treat this academic demo as ready for sensitive legal case data.
