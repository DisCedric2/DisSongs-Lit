from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.
print("welcome")
print("welcome-1")
print("anju jandu")
def DSLhome(req):
    return render(req, "DSLhome.html")


def DSLsignin(req):
    return render(req, "DSLsignin.html")

def DSLsignup(req):
    return render(req, "DSLsignup.html")


def DSLaboutus(req):
    return render(req, "DSLaboutus.html")


def DSLcontactus(req):
    return render(req, "DSLcontactus.html")