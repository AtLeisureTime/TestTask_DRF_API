from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    TEMPLATE = 'index.html'
    MENU_SECTION = 'home'

    return render(request, TEMPLATE, {'section': MENU_SECTION})
