from django.contrib import admin
from django.urls import path
from veniot import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="inicio"),
    path("desarolladores/", views.developers, name="desarrolladores"),
    path("chat/", views.chat, name="chat"),
]
