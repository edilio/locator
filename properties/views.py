# from django.shortcuts import render
from django.shortcuts import redirect

ADMIN_PATH = '/admin'


def home(request):
    return redirect(request.build_absolute_uri(ADMIN_PATH))
