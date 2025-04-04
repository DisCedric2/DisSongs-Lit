from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.conf import settings
from .models import AddSong, UpSong
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ValidationError

# Create your views here.

def index(req):
    allsongs = AddSong.objects.all()
    context = {"allsongs" : allsongs}
    return render(req, "DSLhome.html", context)

def validate_password(password) :
    # check for min length
    if len(password) < 7 :
        raise ValidationError("Password must be atleast 7 characters long :/")
    
    # check for max length
    if len(password) > 99:
        raise ValidationError("Password too long try to fit it under 99 characters :/")
    
    # Initialsing flags for char checks
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    special_characters = "!@#$%^&*~<>?"

    # check for char variety
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in special_characters:
            has_special = True

    if not has_upper:
        raise ValidationError("Password must contain atleast one uppercase letter :/")
    if not has_lower:
        raise ValidationError("Password must contain atleast one lowercase letter :/")
    if not has_digit:
        raise ValidationError("Password must contain atleast one digit :/")
    if not has_special:
        raise ValidationError("Password must contain atleast one special character (eg., !@#$%^&*~<>?) :/")

    # check for commomn passwords
    common_pass = ["password", "1234567", "Qwertyu", "abcd1234"]
    if password in common_pass:
        raise ValidationError("Entered Password is too common :( Please enter unique one :)")
    
def signup(req):
    print(req.method)
    context = {}
    if req.method == "GET":
        return render(req, "DSLsignup.html")
    else:
        print(req.method)
        uname = req.POST["uname"]
        uemail = req.POST["uemail"]
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        print(uname, uemail , upass, ucpass)

        try:
            validate_password(upass)
        except ValidationError as e:
            context["errmsg"] = str(e)
            return render(req, "DSLsignup.html", context)
        
        if uname == "" or upass == "" or ucpass == "":
            context["errmsg"] = "Field cannot be empty :("
            return render(req, "DSLsignup.html", context)
        elif upass != ucpass:
            context["errmsg"] = "Password and Confirm Password aint matching dude :("
            return render(req, "DSLsignup.html", context)
        elif uname.isdigit():
            context["errmsg"] = "Username cannot be only Number smarty :("
            return render(req, "DSLsignup.html", context)
        elif upass == uname:
            context["errmsg"] = "Password cannot be same as Username common dude u r lazy :("
            return render(req, "DSLsignup.html", context)
        else:
            # check for an already user
            if User.objects.filter(username=uname).exists():
                context["errmsg"] = "User already exists :?"
                return render (req, "DSLsignup.html", context)
            else:
                try:
                    userdata = User.objects.create_user(username=uname, password=upass)
                    userdata.save()
                    print(User.objects.all())
                    return redirect("DSLsignin")
                except Exception as e:
                    print("Error creating user")
                    context["errmsg"] = f"Error creating user :{str(e)} :("
                    return render(req, "DSLsignup.html", context)

def signin(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        context = {}
        if uname == "" or upass == "":
            context["errmsg"] = "Field cant be empty :("
            return render(req, "DSLsignin.html", context)
        else:
            userdata = authenticate(username=uname, password=upass)
            #print(req.user.password)
            if userdata is not None:
                login(req, userdata)
                return redirect("DSLhome")
            else:
                context["errmsg"] = "Invalid username and password :("
                return render(req, "DSLsignin.html", context)
    else:
        return render(req, "DSLsignin.html")

def logout_user(req):
    logout(req)
    messages.success(req, "You have successfully logged out :(")
    return redirect("/")

def req_pass_reset(req):
    if req.method == "GET":
        return render(req, "req_pass_reset.html")
    else:
        uname = req.POST.get("uname")
        context = {}
        print(uname)
        try:
            userdata = User.objects.get(username=uname)
            return redirect("reset_pass", uname=userdata.username)
        
        except User.DoesNotExist:
            context["errmsg"] = "No account found with this username"
            return render(req, "req_pass_reset.html", context)
        
def reset_pass(req, uname):
    userdata = User.objects.get(username = uname)
    if req.method == "GET":
        return render(req, "reset_pass.html", {"user" : userdata.username})
    else:
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        context = {}
        userdata = User.objects.get(username=uname)
        try:
            if upass == "" or ucpass == "":
                context["errmsg"] = "Field cannot be empty :("
                return render(req, "reset_pass.html", context)
            elif upass != ucpass:
                context["errmsg"] = "Password and Confirm Password aint Matching Dude :("
                return render(req, "reset_pass.html", context)
            else:
                validate_password(upass)
                userdata.set_password(upass)
                userdata.save()
                return redirect("/DSLsignin")
            
        except ValidationError as e:
            context["errmsg"] = str(e)
            return redirect(req, 'reset_pass.html', context)

'''
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
'''


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
    return redirect("DSLhome")

from django.contrib.auth.decorators import login_required
from .models import AddSong

@login_required(login_url='DSLsignin')
def DSLsong(request, song_id):
    try:
        song = AddSong.objects.get(pk=song_id)
        song.click_count += 1 #increment for top song chart counter
        song.save()
        context = {'song': song}
        return render(request, 'DSLsong.html', context)
    except AddSong.DoesNotExist:
        return redirect('DSLhome')
    
def DSLhome(req):
    top_songs = AddSong.objects.all().order_by('-click_count')[:5]
    songs = AddSong.objects.all()

    is_premium = False
    order_id = ""

    if req.user.is_authenticated:
        # if premium
        premium_subscription = PremiumSubscription.objects.filter(user=req.user, subscription_status=True).first()
        if premium_subscription:
            is_premium = True
        else:
            # If not premium
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
            amount = 9900  # 99 INR in paise
            order = client.order.create({
                "amount": amount,
                "currency": "INR",
                "payment_capture": "1"
            })
            order_id = order["id"]

    context = {
        'songs': songs,
        'top_songs': top_songs,
        'user': req.user,
        'is_premium': is_premium,
        'api_key': settings.RAZORPAY_API_KEY,
        'amount': 9900,
        'order_id': order_id
    }
    return render(req, 'DSLhome.html', context)
    
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

from django.contrib.auth.models import User
users = User.objects.all()
for user in users:
    print(user.username)
