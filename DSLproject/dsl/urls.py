from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("",views.DSLhome, name='DSLhome'),
    path("DSLhome/",views.DSLhome, name='DSLhome'),
    path("DSLsignin/",views.signin, name='DSLsignin'),
    path("DSLsignup/",views.signup, name='DSLsignup'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('req_pass_reset/', views.req_pass_reset, name='req_pass_reset'),
    path('reset_pass/<uname>/', views.reset_pass, name='reset_pass'),
    path("DSLaboutus/",views.DSLaboutus, name='DSLaboutus'),
    path("DSLcontactus/",views.DSLcontactus, name='DSLcontactus'),
    path('DSLsong/<int:song_id>/', views.DSLsong, name='DSLsong'),
    path('DSLupload/', views.DSLupload, name='DSLupload'),
    path("premium/", views.create_payment, name="create_payment"),
    path("premium/success/", views.payment_success, name="payment_success"),
    
]