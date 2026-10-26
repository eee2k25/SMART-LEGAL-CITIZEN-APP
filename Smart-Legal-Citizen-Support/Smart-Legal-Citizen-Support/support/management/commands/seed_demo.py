from django.core.management.base import BaseCommand
from support.models import (
    Category,
    LegalArticle,
    Advocate,
    ComplaintGuide,
    CitizenService,
)


class Command(BaseCommand):
    help = "Load clearly-labelled, repeatable demonstration content (does not create an administrator)."

    def handle(self, *args, **kwargs):
        categories = {}
        for name in [
            "Consumer awareness",
            "Public-service grievances",
            "Cyber safety",
            "General procedures",
        ]:
            categories[name], _ = Category.objects.get_or_create(name=name)
        articles = [
            (
                "Using official sources for legal information",
                "General procedures",
                "This demonstration note explains why users should verify current requirements with an official authority.",
                "Laws and administrative procedures can change. Identify the jurisdiction, date, and issuing authority before relying on a source. This is general educational information, not case-specific advice.",
                "India Code — official central legislation repository",
                "https://www.indiacode.nic.in/",
            ),
            (
                "Preparing to raise a consumer concern",
                "Consumer awareness",
                "A general preparation checklist for organizing a consumer query before contacting the relevant official body.",
                "Keep a clear record of the transaction and dates. Preserve receipts and communications. Write a concise description of the issue and the outcome you are seeking. Check the current process and eligibility on the relevant official consumer portal. This note does not determine legal rights or guarantee an outcome.",
                "National Consumer Helpline",
                "https://consumerhelpline.gov.in/",
            ),
            (
                "Recognizing and reporting online financial fraud",
                "Cyber safety",
                "General safety steps after suspected online financial fraud. Act quickly and use official reporting channels.",
                "Contact your bank or payment provider using verified contact details. Preserve transaction references and communications. Use the official national cybercrime reporting channel and verify current instructions. Do not share passwords, OTPs, or remote access. For immediate danger, contact emergency services.",
                "National Cyber Crime Reporting Portal",
                "https://cybercrime.gov.in/",
            ),
            (
                "Finding public grievance channels",
                "Public-service grievances",
                "An overview of checking the correct department and official grievance channel.",
                "Identify the department responsible for the service. Keep a concise description and any non-sensitive reference number. Use the official grievance portal and save its acknowledgment. Do not treat this platform as having filed a grievance.",
                "CPGRAMS — official public grievance portal",
                "https://pgportal.gov.in/",
            ),
        ]
        for title, cat, summary, content, source, url in articles:
            LegalArticle.objects.update_or_create(
                slug=title.lower().replace(" ", "-"),
                defaults={
                    "title": title,
                    "category": categories[cat],
                    "summary": summary,
                    "content": content,
                    "jurisdiction": "India",
                    "language": "English",
                    "source_title": source,
                    "source_url": url,
                    "published": True,
                },
            )
        guides = [
            (
                "Preparing a consumer grievance",
                "Consumer",
                "Organize relevant information before using the official channel. This guide is general and does not submit anything for you.",
                "Identify the seller and issue\nCollect receipts and relevant communications\nWrite a concise timeline and requested resolution\nCheck current eligibility and submit through the official portal if appropriate",
                "Receipts or transaction records\nRelevant messages or correspondence\nA concise timeline of events",
                "https://consumerhelpline.gov.in/",
                "National Consumer Helpline",
                "https://consumerhelpline.gov.in/",
            ),
            (
                "Reporting a suspected cybercrime",
                "Cyber safety",
                "Use the official portal and follow its current instructions. Do not delay urgent contact with your bank.",
                "Contact your bank or payment provider through verified channels\nPreserve transaction references and evidence\nUse the official cybercrime reporting portal\nFollow instructions from the relevant authority",
                "Transaction or complaint references\nRelevant screenshots or communications\nDates and a short incident summary",
                "https://cybercrime.gov.in/",
                "National Cyber Crime Reporting Portal",
                "https://cybercrime.gov.in/",
            ),
        ]
        for title, cat, summary, steps, checks, portal, source, sourceurl in guides:
            ComplaintGuide.objects.update_or_create(
                slug=title.lower().replace(" ", "-"),
                defaults={
                    "title": title,
                    "category": cat,
                    "summary": summary,
                    "steps": steps,
                    "checklist": checks,
                    "portal_url": portal,
                    "source_title": source,
                    "source_url": sourceurl,
                    "published": True,
                },
            )
        services = [
            (
                "National Consumer Helpline",
                "Consumer affairs",
                "Consumer Affairs Department",
                "Official consumer information and grievance channel. Check the portal for current process and contact options.",
                "India",
                "https://consumerhelpline.gov.in/",
                "National Consumer Helpline",
            ),
            (
                "CPGRAMS Public Grievances",
                "Public grievance",
                "Government of India",
                "Official portal for public grievances. Confirm applicability and current process on the official website.",
                "India",
                "https://pgportal.gov.in/",
                "CPGRAMS",
            ),
            (
                "National Cyber Crime Reporting Portal",
                "Cyber safety",
                "Ministry of Home Affairs",
                "Official portal for reporting cybercrime. For immediate financial fraud response, also contact your bank using verified details.",
                "India",
                "https://cybercrime.gov.in/",
                "National Cyber Crime Reporting Portal",
            ),
        ]
        for name, cat, dept, desc, jur, url, source in services:
            CitizenService.objects.update_or_create(
                slug=name.lower().replace(" ", "-"),
                defaults={
                    "name": name,
                    "category": cat,
                    "department": dept,
                    "description": desc,
                    "jurisdiction": jur,
                    "official_url": url,
                    "source_title": source,
                    "published": True,
                },
            )
        for name, area, city in [
            ("Aarav Demo Advocate", "Consumer law, general civil queries", "Hyderabad"),
            (
                "Meera Sample Advocate",
                "Employment and public-service queries",
                "Hyderabad",
            ),
        ]:
            Advocate.objects.update_or_create(
                slug=name.lower().replace(" ", "-"),
                defaults={
                    "name": name,
                    "practice_areas": area,
                    "city": city,
                    "region": "Telangana",
                    "verification_status": "pending",
                    "demo_record": True,
                    "is_public": True,
                    "bio": "Fictional profile created solely for application demonstration. Not a real advocate; do not use for contact or legal representation.",
                },
            )
        self.stdout.write(
            self.style.SUCCESS(
                "Demo content loaded or updated. Fictional directory profiles are labelled; no admin account was created."
            )
        )
