from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.conf import settings
from .models import AddSong
# Create your views here.
print("welcome")
print("welcome-1")
print("anju jandu")
def DSLhome(req):
    songs = AddSong.objects.all()
    return render(req, "DSLhome.html", {"songs":songs})


def DSLsignin(req):
    return render(req, "DSLsignin.html")

def DSLsignup(req):
    return render(req, "DSLsignup.html")


def DSLaboutus(req):
    return render(req, "DSLaboutus.html")


def DSLcontactus(req):
    return render(req, "DSLcontactus.html")




import razorpay
from . models import PremiumSubscription
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def create_payment(req):
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
    amount = 9900 # Amount in paise (10000 = 100 INR)

    payment = client.order.create({
        "amount" : amount,
        "currency" : "INR",
        "payment_capture" : "1"
    })

    subscription, created = PremiumSubscription.objects.get_or_create(user=req.user)
    subscription.payment_id = payment["id"]
    subscription.save()

    return render(req, "payment.html", {
        "api_key" : settings.RAZORPAY_API_KEY,
        "order_id" : payment["id"],
        "amount" : amount,
        "user" : req.user,
    })

@login_required
def payment_success(req):
    if req.method == "POST":
        payment_id = req.POST.get("razorpay_payment_id")
        subscription = PremiumSubscription.objects.get(user=req.user)
        subscription.payment_id = payment_id
        subscription.subscription_status = True
        subscription.save()
        return HttpResponse("PAYMENT SUCCESSFULL :)")
    return redirect("DSLhome")