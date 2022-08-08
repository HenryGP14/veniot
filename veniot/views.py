from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def developers(request):
    return render(request, "developers.html")


def chat(request):
    return render(request, "chat.html")
