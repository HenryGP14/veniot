from operator import truediv
from django.shortcuts import render

from entrenamiento.models import Media


def index(request):
    return render(request, "index.html")


def developers(request):
    return render(request, "developers.html")


def chat(request):
    return render(request, "chat.html")
