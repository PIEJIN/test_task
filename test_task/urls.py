
from django.contrib import admin
from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("meetings.urls", namespace="api")),
]