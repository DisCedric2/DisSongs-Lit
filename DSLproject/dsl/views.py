from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.conf import settings
from .models import AddSong
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if User is not None:
            login(request, User)
            messages.success(request, f"Welcome back, {username}!")
            return redirect("DSLhome")  # Redirect to homepage after login
        else:
            messages.error(request, "Invalid username or password")
            return redirect("DSLsignin")
    
    return render(request, "DSLsignin.html")

def logout_user(req):
    logout(req)
    messages.success(req, "You have successfully logged out.")
    return redirect("DSLhome.html")


print("welcome")

print("anju jandu")

def DSLhome(req):
    songs = AddSong.objects.all()
    context = {'songs': songs}
    return render(req, 'DSLhome.html', context)


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

from django.contrib.auth.decorators import login_required
from .models import AddSong

@login_required(login_url='DSLsignin')
def DSLsong(request, song_id):
    try:
        song = AddSong.objects.get(pk=song_id)
        context = {'song': song}
        return render(request, 'DSLsong.html', context)
    except AddSong.DoesNotExist:
        return redirect('DSLhome')
    
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url='DSLsignin')
def DSLupload(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        artist = request.POST.get('artist')
        description = request.POST.get('description')
        lyrics = request.POST.get('lyrics')
        video_url = request.POST.get('video_url')
        image = request.FILES.get('image')

        song = AddSong.objects.create(
            title=title,
            artist=artist,
            description=description,
            lyrics=lyrics,
            video_url=video_url,
            image=image,
            uploaded_by=request.user  
        )
        song.save()
        return redirect('DSLsong', song_id=song.id)

    return render(request, 'DSLupload.html')
