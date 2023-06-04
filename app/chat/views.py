from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse


@login_required
def chatRoom(request: HttpRequest) -> HttpResponse:
    TEMPLATE = 'chat/room.html'
    MENU_SECTION = 'chat_room'

    return render(request, TEMPLATE, {'section': MENU_SECTION})
