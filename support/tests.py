from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from django.core.management import call_command
from django.test import override_settings
from .models import (
    Category,
    LegalArticle,
    Bookmark,
    Feedback,
    ComplaintGuide,
    SavedChecklist,
)


class PlatformTests(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="Consumer")
        self.article = LegalArticle.objects.create(
            title="Consumer guide",
            slug="consumer-guide",
            summary="Consumer info",
            content="Relevant consumer content",
            category=self.cat,
            published=True,
        )
        self.user = User.objects.create_user(
            username="citizen", password="StrongPassword123!", email="c@example.com"
        )

    def test_public_legal_search(self):
        response = self.client.get(reverse("legal_list"), {"q": "consumer"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Consumer guide")

    def test_legal_search_matches_keywords_without_exact_phrase(self):
        property_category = Category.objects.create(name="Property and land")
        article = LegalArticle.objects.create(
            title="Land records overview",
            slug="land-records-overview",
            summary="A general guide to checking records",
            content="Verify current property requirements with official sources.",
            category=property_category,
            published=True,
        )
        response = self.client.get(reverse("legal_list"), {"q": "law property"})
        self.assertContains(response, article.title)

    def test_legal_search_matches_domestic_violence_words(self):
        article = LegalArticle.objects.create(
            title="Domestic violence: safety information",
            slug="domestic-violence-safety",
            summary="General information and verified support sources.",
            content="This article is about domestic abuse and personal safety.",
            category=self.cat,
            published=True,
        )
        response = self.client.get(
            reverse("legal_list"), {"q": "violence domestic"}
        )
        self.assertContains(response, article.title)

    def test_advocate_search_uses_practice_area_keywords(self):
        from .models import Advocate

        Advocate.objects.create(
            name="Verified Example Profile",
            slug="verified-example-profile",
            practice_areas="Property law and conveyancing",
            city="Hyderabad",
            region="Telangana",
            is_public=True,
        )
        response = self.client.get(reverse("advocates"), {"q": "law property"})
        self.assertContains(response, "Verified Example Profile")

    def test_seeded_slugs_fit_database_field_limit(self):
        call_command("seed_demo")
        seed_titles = [
            "Cyber law in India: online offences and reporting",
            "Property and land transactions: an India and Telangana starting point",
            "Domestic violence: the central law and support options",
        ]
        seeded = LegalArticle.objects.filter(title__in=seed_titles)
        self.assertEqual(seeded.count(), 3)
        self.assertTrue(all(len(slug) <= 50 for slug in seeded.values_list("slug", flat=True)))

    def test_draft_not_public(self):
        draft = LegalArticle.objects.create(
            title="Secret draft",
            slug="secret-draft",
            summary="Draft",
            content="Hidden",
            category=self.cat,
            published=False,
        )
        self.assertEqual(
            self.client.get(reverse("legal_detail", args=[draft.slug])).status_code, 404
        )

    def test_legal_jurisdiction_language_filters(self):
        LegalArticle.objects.create(
            title="Telugu legal note",
            slug="telugu-note",
            summary="regional",
            content="regional information",
            category=self.cat,
            published=True,
            jurisdiction="Telangana",
            language="Telugu",
        )
        response = self.client.get(
            reverse("legal_list"), {"jurisdiction": "Telangana", "language": "Telugu"}
        )
        self.assertContains(response, "Telugu legal note")
        self.assertNotContains(response, "Consumer guide")

    def test_registration_hashes_password(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newcitizen",
                "first_name": "New Citizen",
                "email": "new@example.com",
                "password1": "StrongXyZ12345!",
                "password2": "StrongXyZ12345!",
                "terms": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        created = User.objects.get(username="newcitizen")
        self.assertNotEqual(created.password, "StrongXyZ12345!")
        self.assertTrue(created.check_password("StrongXyZ12345!"))

    def test_duplicate_email_rejected(self):
        r = self.client.post(
            reverse("register"),
            {
                "username": "another",
                "first_name": "Another",
                "email": "C@Example.com",
                "password1": "StrongXyZ12345!",
                "password2": "StrongXyZ12345!",
                "terms": "on",
            },
        )
        self.assertEqual(r.status_code, 200)
        self.assertFalse(User.objects.filter(username="another").exists())

    def test_dashboard_requires_auth(self):
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 302)

    def test_normal_user_cannot_access_admin(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse("admin:index")).status_code, 302)

    def test_logout_ends_authenticated_session(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn("_auth_user_id", self.client.session)

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_password_reset_request_uses_configured_email_backend(self):
        response = self.client.post(
            reverse("password_reset"), {"email": "c@example.com"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("/account/reset/", mail.outbox[0].body)

    def test_bookmark_ownership_and_post(self):
        self.client.force_login(self.user)
        r = self.client.post(reverse("bookmark", args=[self.article.slug]))
        self.assertEqual(r.status_code, 302)
        self.assertTrue(
            Bookmark.objects.filter(user=self.user, article=self.article).exists()
        )

    def test_saved_are_user_scoped(self):
        other = User.objects.create_user(
            username="other", password="StrongPassword123!"
        )
        Bookmark.objects.create(user=other, article=self.article)
        self.client.force_login(self.user)
        r = self.client.get(reverse("saved"))
        self.assertNotContains(r, "Consumer guide")

    def test_feedback_submission(self):
        r = self.client.post(
            reverse("feedback"),
            {
                "category": "site",
                "subject": "Test",
                "message": "Useful feedback",
                "email": "",
            },
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Feedback.objects.count(), 1)

    def test_assistant_searches_published_library(self):
        self.client.force_login(self.user)
        r = self.client.post(
            reverse("assistant"), {"question": "consumer legal information"}
        )
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Consumer guide")

    def test_checklist_is_user_scoped(self):
        guide = ComplaintGuide.objects.create(
            title="Private Guide",
            slug="private-guide",
            category="General",
            summary="Summary",
            steps="Step",
            checklist="Keep a copy",
        )
        other = User.objects.create_user(
            username="checklist-owner", password="StrongPassword123!"
        )
        SavedChecklist.objects.create(user=other, guide=guide)
        self.client.force_login(self.user)
        response = self.client.get(reverse("saved"))
        self.assertNotContains(response, "Private Guide")
        self.assertEqual(SavedChecklist.objects.filter(user=self.user).count(), 0)

    def test_account_deletion_removes_saved_items(self):
        Bookmark.objects.create(user=self.user, article=self.article)
        self.client.force_login(self.user)
        r = self.client.post(reverse("delete_account"))
        self.assertEqual(r.status_code, 302)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
        self.assertEqual(Bookmark.objects.count(), 0)
