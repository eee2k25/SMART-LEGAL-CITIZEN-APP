from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *a, **kw):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*a, **kw)

    def __str__(self):
        return self.name


class LegalArticle(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.CharField(max_length=350)
    content = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="articles"
    )
    jurisdiction = models.CharField(max_length=100, default="India")
    language = models.CharField(max_length=40, default="English")
    source_title = models.CharField(max_length=180, blank=True)
    source_url = models.URLField(blank=True)
    last_reviewed = models.DateField(null=True, blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        indexes = [models.Index(fields=["published", "category"])]

    def save(self, *a, **kw):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*a, **kw)

    def __str__(self):
        return self.title


class Advocate(models.Model):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    REVIEW = "review"
    STATUS = [
        (PENDING, "Pending"),
        (VERIFIED, "Verified"),
        (REJECTED, "Rejected"),
        (REVIEW, "Needs review"),
    ]
    name = models.CharField(max_length=140)
    slug = models.SlugField(unique=True, blank=True)
    bio = models.TextField(blank=True)
    practice_areas = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100, default="Telangana")
    public_email = models.EmailField(blank=True)
    public_phone = models.CharField(max_length=30, blank=True)
    verification_status = models.CharField(
        max_length=16, choices=STATUS, default=PENDING
    )
    demo_record = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def save(self, *a, **kw):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*a, **kw)

    def __str__(self):
        return self.name


class ComplaintGuide(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=100)
    jurisdiction = models.CharField(max_length=100, default="India")
    summary = models.TextField()
    steps = models.TextField(help_text="One step per line")
    checklist = models.TextField(help_text="One item per line")
    portal_url = models.URLField(blank=True)
    source_title = models.CharField(max_length=180, blank=True)
    source_url = models.URLField(blank=True)
    last_reviewed = models.DateField(null=True, blank=True)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]

    def save(self, *a, **kw):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*a, **kw)

    def __str__(self):
        return self.title


class CitizenService(models.Model):
    name = models.CharField(max_length=180)
    slug = models.SlugField(unique=True, blank=True)
    department = models.CharField(max_length=180, blank=True)
    category = models.CharField(max_length=100)
    description = models.TextField()
    jurisdiction = models.CharField(max_length=100, default="India")
    official_url = models.URLField(blank=True)
    source_title = models.CharField(max_length=180, blank=True)
    last_reviewed = models.DateField(null=True, blank=True)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def save(self, *a, **kw):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*a, **kw)

    def __str__(self):
        return self.name


class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookmarks"
    )
    article = models.ForeignKey(
        LegalArticle, on_delete=models.CASCADE, related_name="bookmarks"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("user", "article")]


class SavedChecklist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="checklists"
    )
    guide = models.ForeignKey(ComplaintGuide, on_delete=models.CASCADE)
    completed_items = models.JSONField(default=list, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("user", "guide")]


class Feedback(models.Model):
    STATUS = [("new", "New"), ("reviewing", "Reviewing"), ("resolved", "Resolved")]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    category = models.CharField(max_length=40)
    subject = models.CharField(max_length=140)
    message = models.TextField(max_length=2000)
    email = models.EmailField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.subject
