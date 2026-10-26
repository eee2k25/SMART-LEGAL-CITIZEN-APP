from django.contrib import admin
from django.urls import path, include
from support import views

handler403 = views.error403
handler404 = views.error404
handler500 = views.error500
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("support.urls")),
]
