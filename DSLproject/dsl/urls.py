from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home Page
    path("", views.DSLhome, name='DSLhome'),

    # Authentication
    path("DSLsignin/", views.signin, name='DSLsignin'),
    path("DSLsignup/", views.signup, name='DSLsignup'),
    path("logout_user/", views.logout_user, name='logout_user'),

    # Password Reset
    path("req_pass_reset/", views.req_pass_reset, name='req_pass_reset'),
    path("reset_pass/<str:uname>/", views.reset_pass, name='reset_pass'),

    # Other Pages
    path("DSLaboutus/", views.DSLaboutus, name='DSLaboutus'),
    path("DSLcontactus/", views.DSLcontactus, name='DSLcontactus'),

    # Song-Related Pages
    path("DSLsong/<int:song_id>/", views.DSLsong, name='DSLsong'),
    path("DSLupload/", views.DSLupload, name='DSLupload'),

    # Payment (Razorpay)
    path("premium/", views.create_payment, name="create_payment"),
    path("premium/success/", views.payment_success, name="payment_success"),
]
