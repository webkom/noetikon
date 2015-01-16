# -*- coding: utf8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def home(request):
    print(request.user)
    print(request.user.is_authenticated())
    return hhome(request)

@login_required
def hhome(request):
    return HttpResponse("success")
