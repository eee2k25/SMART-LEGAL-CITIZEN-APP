# Testing

## Run

```bash
python manage.py test
python manage.py check
```

## Test cases in `support/tests.py`

1. Public library search returns a matching article.
2. Unpublished article detail is not public (404).
3. Registration creates an account and stores a Django-hashed password.
4. Duplicate email is rejected.
5. Anonymous dashboard request redirects to login.
6. Authenticated bookmark POST stores a user/article relation.
7. Saved page does not reveal another user's bookmark.
8. Feedback POST is persisted.
9. Assistant search returns matching published-library content.
10. Another user's saved checklist is not shown.
11. Account deletion removes the account and cascades to saved items.
12. Legal language and jurisdiction filters narrow results correctly.
13. A normal citizen cannot access Django admin.
14. CSRF-protected logout ends the authenticated session.
15. Password-reset request sends a token email through the configured backend (tested with Django's local-memory test backend).

## Actual execution in the development workspace

`python manage.py test` was run after migration and seed command: **15 tests passed**; Django reported no system-check issues at that point. The project is tested with Django's built-in test client, not a real browser automation engine. A local HTTP smoke test against the running server returned 200 for the homepage, legal search, and CSS asset; a broader Django test-client smoke run returned 200 for public list/detail pages. Responsive behavior was reviewed from CSS breakpoints but not visually browser-tested at every viewport. The test suite does not claim real SMTP delivery, exhaustive admin/model permissions, PostgreSQL integration, production static assets, accessibility audits, or load performance.

After deployment, rerun tests against the deployed build and exercise password-reset email, HTTPS, host, static-file, and database behavior using the real provider configuration.
