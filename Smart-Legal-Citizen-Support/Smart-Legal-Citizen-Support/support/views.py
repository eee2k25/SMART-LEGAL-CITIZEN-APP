from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import RegisterForm, ProfileForm, FeedbackForm
from .models import (
    LegalArticle,
    Category,
    Advocate,
    ComplaintGuide,
    CitizenService,
    Bookmark,
    SavedChecklist,
)


def home(request):
    return render(
        request,
        "support/home.html",
        {
            "featured": LegalArticle.objects.filter(published=True).order_by(
                "-updated_at"
            )[:3],
            "categories": Category.objects.all()[:6],
        },
    )


def about(request):
    return render(request, "support/about.html")


def legal_list(request):
    q = request.GET.get("q", "").strip()[:100]
    category = request.GET.get("category", "")
    language = request.GET.get("language", "").strip()[:40]
    jurisdiction = request.GET.get("jurisdiction", "").strip()[:100]
    qs = LegalArticle.objects.filter(published=True).select_related("category")
    if q:
        qs = qs.filter(
            Q(title__icontains=q) | Q(summary__icontains=q) | Q(content__icontains=q)
        )
    if category:
        qs = qs.filter(category__slug=category)
    if language:
        qs = qs.filter(language__iexact=language)
    if jurisdiction:
        qs = qs.filter(jurisdiction__iexact=jurisdiction)
    languages = (
        LegalArticle.objects.filter(published=True)
        .values_list("language", flat=True)
        .distinct()
        .order_by("language")
    )
    jurisdictions = (
        LegalArticle.objects.filter(published=True)
        .values_list("jurisdiction", flat=True)
        .distinct()
        .order_by("jurisdiction")
    )
    return render(
        request,
        "support/legal_list.html",
        {
            "page_obj": Paginator(qs, 8).get_page(request.GET.get("page")),
            "q": q,
            "categories": Category.objects.all(),
            "selected_category": category,
            "language": language,
            "languages": languages,
            "jurisdiction": jurisdiction,
            "jurisdictions": jurisdictions,
        },
    )


def legal_detail(request, slug):
    item = get_object_or_404(LegalArticle, slug=slug, published=True)
    saved = (
        request.user.is_authenticated
        and Bookmark.objects.filter(user=request.user, article=item).exists()
    )
    related = LegalArticle.objects.filter(
        published=True, category=item.category
    ).exclude(pk=item.pk)[:3]
    return render(
        request,
        "support/legal_detail.html",
        {"item": item, "saved": saved, "related": related},
    )


@login_required
@require_POST
def bookmark(request, slug):
    article = get_object_or_404(LegalArticle, slug=slug, published=True)
    obj, created = Bookmark.objects.get_or_create(user=request.user, article=article)
    if not created:
        obj.delete()
        messages.success(request, "Removed from saved legal information.")
    else:
        messages.success(request, "Saved to your legal information.")
    return redirect("legal_detail", slug=slug)


def advocate_list(request):
    q = request.GET.get("q", "").strip()[:100]
    city = request.GET.get("city", "").strip()[:80]
    verified = request.GET.get("verified", "")
    qs = Advocate.objects.filter(is_public=True)
    if q:
        qs = qs.filter(
            Q(name__icontains=q) | Q(practice_areas__icontains=q) | Q(bio__icontains=q)
        )
    if city:
        qs = qs.filter(Q(city__icontains=city) | Q(region__icontains=city))
    if verified == "yes":
        qs = qs.filter(verification_status="verified")
    return render(
        request,
        "support/advocates.html",
        {
            "page_obj": Paginator(qs, 9).get_page(request.GET.get("page")),
            "q": q,
            "city": city,
            "verified": verified,
        },
    )


def advocate_detail(request, slug):
    return render(
        request,
        "support/advocate_detail.html",
        {"item": get_object_or_404(Advocate, slug=slug, is_public=True)},
    )


def guide_list(request):
    q = request.GET.get("q", "").strip()[:100]
    qs = ComplaintGuide.objects.filter(published=True)
    if q:
        qs = qs.filter(
            Q(title__icontains=q) | Q(category__icontains=q) | Q(summary__icontains=q)
        )
    return render(
        request,
        "support/guides.html",
        {"page_obj": Paginator(qs, 8).get_page(request.GET.get("page")), "q": q},
    )


def guide_detail(request, slug):
    guide = get_object_or_404(ComplaintGuide, slug=slug, published=True)
    checklist = None
    if request.user.is_authenticated:
        checklist = SavedChecklist.objects.filter(
            user=request.user, guide=guide
        ).first()
    return render(
        request, "support/guide_detail.html", {"item": guide, "checklist": checklist}
    )


@login_required
@require_POST
def checklist_toggle(request, slug):
    guide = get_object_or_404(ComplaintGuide, slug=slug, published=True)
    index = request.POST.get("index", "")
    try:
        index = int(index)
    except ValueError:
        return redirect("guide_detail", slug=slug)
    items = guide.checklist.splitlines()
    saved, _ = SavedChecklist.objects.get_or_create(user=request.user, guide=guide)
    if 0 <= index < len(items):
        done = set(saved.completed_items)
        if index in done:
            done.remove(index)
        else:
            done.add(index)
        saved.completed_items = sorted(done)
        saved.save()
    return redirect("guide_detail", slug=slug)


def services(request):
    q = request.GET.get("q", "").strip()[:100]
    category = request.GET.get("category", "").strip()[:80]
    qs = CitizenService.objects.filter(published=True)
    if q:
        qs = qs.filter(
            Q(name__icontains=q)
            | Q(description__icontains=q)
            | Q(department__icontains=q)
        )
    if category:
        qs = qs.filter(category__icontains=category)
    categories = (
        CitizenService.objects.filter(published=True)
        .values_list("category", flat=True)
        .distinct()
    )
    return render(
        request,
        "support/services.html",
        {
            "page_obj": Paginator(qs, 8).get_page(request.GET.get("page")),
            "q": q,
            "category": category,
            "categories": categories,
        },
    )


def service_detail(request, slug):
    return render(
        request,
        "support/service_detail.html",
        {"item": get_object_or_404(CitizenService, slug=slug, published=True)},
    )


def emergency(request):
    return render(request, "support/emergency.html")


def contact(request):
    return render(request, "support/contact.html")


def feedback(request):
    form = FeedbackForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user if request.user.is_authenticated else None
        obj.save()
        messages.success(
            request, "Thank you. Your feedback has been recorded for review."
        )
        return redirect("feedback")
    return render(request, "support/feedback.html", {"form": form})


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account is ready.")
        return redirect("dashboard")
    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard(request):
    return render(
        request,
        "support/dashboard.html",
        {
            "bookmarks": Bookmark.objects.filter(user=request.user).select_related(
                "article"
            )[:5],
            "checklists": SavedChecklist.objects.filter(
                user=request.user
            ).select_related("guide")[:5],
        },
    )


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect("profile")
    return render(request, "support/profile.html", {"form": form})


@login_required
def delete_account(request):
    if request.method == "POST":
        from django.contrib.auth import logout

        user = request.user
        logout(request)
        user.delete()  # User-owned bookmarks/checklists cascade; feedback remains without the user link.
        messages.success(
            request, "Your account and user-owned saved items have been deleted."
        )
        return redirect("home")
    return render(request, "support/delete_account.html")


@login_required
def saved(request):
    return render(
        request,
        "support/saved.html",
        {
            "bookmarks": Bookmark.objects.filter(user=request.user).select_related(
                "article"
            ),
            "checklists": SavedChecklist.objects.filter(
                user=request.user
            ).select_related("guide"),
        },
    )


@login_required
def assistant(request):
    answer = None
    results = []
    query = ""
    if request.method == "POST":
        query = request.POST.get("question", "").strip()[:500]
        if len(query) < 4:
            answer = "Please enter a little more detail so I can search the reviewed information."
        else:
            terms = [w for w in query.lower().split() if len(w) > 3][:8]
            qs = LegalArticle.objects.filter(published=True)
            match = Q()
            for term in terms:
                match |= (
                    Q(title__icontains=term)
                    | Q(summary__icontains=term)
                    | Q(content__icontains=term)
                )
            results = list(qs.filter(match).distinct()[:4]) if terms else []
            answer = (
                "I found the following reviewed information that may be relevant. Please check its jurisdiction and source. This is general information, not legal advice."
                if results
                else "I could not find a sufficiently relevant reviewed article in the current library. Please consult a qualified lawyer or the appropriate authority; for immediate danger, use verified emergency services."
            )
    return render(
        request,
        "support/assistant.html",
        {"answer": answer, "results": results, "query": query},
    )


def privacy(request):
    return render(
        request,
        "support/policy.html",
        {
            "title": "Privacy policy",
            "body": "We collect only information needed to operate this demonstration platform. Account details and saved items are stored in the application database. Feedback is visible only to authorized administrators. Avoid submitting confidential case facts. Development deployments may use local SQLite and console email. Request account assistance through the project administrator. Retention and deletion are subject to operational and applicable legal requirements.",
        },
    )


def terms(request):
    return render(
        request,
        "support/policy.html",
        {
            "title": "Terms and conditions",
            "body": "Use this platform lawfully and do not submit confidential or unnecessary sensitive information. Content is general educational information, not legal advice. Government and external links are provided for convenience; verify current details with the official source. No filing, contact, case update, or professional verification is implied unless explicitly stated.",
        },
    )


def disclaimer(request):
    return render(
        request,
        "support/policy.html",
        {
            "title": "Legal-information disclaimer",
            "body": "This platform provides general legal information and citizen-service guidance for educational use. It is not a substitute for advice from a qualified lawyer or an official authority. Laws and procedures change; verify current requirements with an authoritative source. The assistant searches curated platform content and does not provide legal advice or guarantee outcomes.",
        },
    )


def error403(request, exception=None):
    return render(
        request,
        "support/error.html",
        {"code": "403", "message": "You do not have permission to view this page."},
        status=403,
    )


def error404(request, exception=None):
    return render(
        request,
        "support/error.html",
        {"code": "404", "message": "We could not find that page."},
        status=404,
    )


def error500(request):
    return render(
        request,
        "support/error.html",
        {"code": "500", "message": "Something went wrong. Please try again later."},
        status=500,
    )
