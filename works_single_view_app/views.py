from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, "works_single_view_app/home.html")


def about(request):
    return render(request, "works_single_view_app/about.html")


def contact(request):
    return render(request, "works_single_view_app/contact.html")


def hello_there(request, name):
    return render(
        request,
        'hello/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )
