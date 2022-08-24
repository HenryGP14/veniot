from django.contrib import admin
from django.urls import path
from veniot import views
from django.conf import settings
from django.conf.urls.static import static

from entrenamiento import views as vw_en


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", views.index, name="inicio"),
        path("desarolladores/", views.developers, name="desarrolladores"),
        path("chat/", views.chat, name="chat"),
        path("clonar/", vw_en.clonar, name="clonar"),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
