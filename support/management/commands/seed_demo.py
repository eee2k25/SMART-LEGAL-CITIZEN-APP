from django.core.management.base import BaseCommand
from django.utils.text import slugify
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
            "Property and land",
            "Domestic violence and safety",
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
            (
                "Cyber law in India: online offences and reporting",
                "Cyber safety",
                "A starting point for cyber law, the Information Technology Act, online offences, hacking, digital fraud, and cybercrime reporting in India.",
                "India's Information Technology Act, 2000 is a central law concerning electronic records and communications and certain computer-related matters. The applicable provisions depend on the facts and the current law, including amendments and rules; this article does not decide whether conduct is an offence or provide case-specific advice. For suspected online financial fraud, contact your bank or payment provider using verified details, preserve relevant records, and check the official National Cyber Crime Reporting Portal for current instructions. Never share passwords, OTPs, or remote-access codes. This platform does not file a complaint.",
                "India Code — Information Technology Act, 2000",
                "https://www.indiacode.nic.in/handle/123456789/1362/simple-search?query=The+Information+Technology+Act%2C+2000",
            ),
            (
                "Property and land transactions: an India and Telangana starting point",
                "Property and land",
                "Search reference for property law, land, ownership, buying or selling, leases, transfer of property, title documents, registration, and Telangana records. Property rules depend on the state and transaction.",
                "Property questions may involve several central and state laws, the type of property, and the facts. The Transfer of Property Act, 1882 is one central statute, but it is not a complete guide to every land, inheritance, tenancy, registration, or revenue issue. For Telangana registration information, use the official Telangana Registration & Stamps Department portal and verify what each record does and does not prove. Do not rely on a single online record as a guarantee of ownership or clear title. Before signing or paying, verify current requirements with official sources and consider advice from a qualified lawyer. This article is general information, not legal advice.",
                "India Code — Transfer of Property Act, 1882",
                "https://www.indiacode.nic.in/bitstream/123456789/14037/1/transfer_of_property_act8_(1).pdf",
            ),
            (
                "Domestic violence: the central law and support options",
                "Domestic violence and safety",
                "India-specific starting information for domestic abuse or family violence and the Protection of Women from Domestic Violence Act, 2005. This page is not an emergency service or legal advice.",
                "The Protection of Women from Domestic Violence Act, 2005 is a central Indian law relevant to domestic violence. It provides a legal framework that includes procedures and possible orders through the competent authorities and courts. Whether the Act or any remedy applies depends on the facts and current law. Read the official Act and contact a qualified lawyer, the appropriate Protection Officer, or a trusted support organisation for help with a specific situation. If someone is in immediate danger, contact local emergency services or police. Consider personal safety before using a shared device; this website does not alert authorities or submit a complaint.",
                "India Code — Protection of Women from Domestic Violence Act, 2005",
                "https://indiacode.nic.in/handle/123456789/12904?sam_handle=",
            ),
        ]
        for title, cat, summary, content, source, url in articles:
            LegalArticle.objects.update_or_create(
                slug=slugify(title),
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
                slug=slugify(title),
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
            (
                "Telangana Registration & Stamps Department",
                "Property and land",
                "Government of Telangana",
                "Official Telangana portal with property registration information and online services such as market value and encumbrance searches. Check the portal for current availability, scope, and requirements; an online record alone does not guarantee ownership or title.",
                "Telangana",
                "https://www.registration.telangana.gov.in/",
                "Telangana Registration & Stamps Department",
            ),
        ]
        for name, cat, dept, desc, jur, url, source in services:
            CitizenService.objects.update_or_create(
                slug=slugify(name),
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
                slug=slugify(name),
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
