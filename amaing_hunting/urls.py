from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from vacancies import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", views.hello),
    path("vacancy/", include("vacancies.urls")),
    path("company/", include("companies.urls")),
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
