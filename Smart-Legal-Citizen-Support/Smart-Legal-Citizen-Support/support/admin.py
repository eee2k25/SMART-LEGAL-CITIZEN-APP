from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    Category,
    LegalArticle,
    Advocate,
    ComplaintGuide,
    CitizenService,
    Bookmark,
    SavedChecklist,
    Feedback,
)


@admin.register(LegalArticle)
class LegalArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "jurisdiction", "published", "last_reviewed")
    list_filter = ("published", "category", "jurisdiction")
    search_fields = ("title", "summary", "content")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Advocate)
class AdvocateAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "verification_status", "demo_record", "is_public")
    list_filter = ("verification_status", "city", "demo_record")
    search_fields = ("name", "practice_areas")
    readonly_fields = ()


@admin.register(ComplaintGuide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published")
    list_filter = ("category", "published")
    search_fields = ("title", "summary")


@admin.register(CitizenService)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "department", "published")
    list_filter = ("category", "published")
    search_fields = ("name", "department")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("subject", "category", "status", "created_at")
    list_filter = ("status", "category")
    search_fields = ("subject", "message")
    readonly_fields = ("user", "created_at")


admin.site.register([Category, Bookmark, SavedChecklist])
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
