from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, "pages/home.html")

def about(request):
    context = {"name": "chiikawa"}
    return render(request, "pages/about.html", context)
