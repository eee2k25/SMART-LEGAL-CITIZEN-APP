from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("legal/", views.legal_list, name="legal_list"),
    path("legal/<slug:slug>/", views.legal_detail, name="legal_detail"),
    path("legal/<slug:slug>/save/", views.bookmark, name="bookmark"),
    path("advocates/", views.advocate_list, name="advocates"),
    path("advocates/<slug:slug>/", views.advocate_detail, name="advocate_detail"),
    path("complaints/", views.guide_list, name="guides"),
    path("complaints/<slug:slug>/", views.guide_detail, name="guide_detail"),
    path(
        "complaints/<slug:slug>/checklist/",
        views.checklist_toggle,
        name="checklist_toggle",
    ),
    path("services/", views.services, name="services"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("emergency/", views.emergency, name="emergency"),
    path("contact/", views.contact, name="contact"),
    path("feedback/", views.feedback, name="feedback"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("account/delete/", views.delete_account, name="delete_account"),
    path("saved/", views.saved, name="saved"),
    path("assistant/", views.assistant, name="assistant"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
    path("disclaimer/", views.disclaimer, name="disclaimer"),
    path(
        "account/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("account/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "account/password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "account/password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "account/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "account/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
