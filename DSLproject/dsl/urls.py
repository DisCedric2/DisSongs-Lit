from django.urls import path
from . import views

urlpatterns = [
    path("",views.DSLhome, name='DSLhome'),
    path("DSLsignup/",views.DSLsignup, name='DSLsignup'),
    path("DSLsignin/",views.DSLsignin, name='DSLsignin'),
    path("DSLaboutus/",views.DSLaboutus, name='DSLaboutus'),
    path("DSLcontactus/",views.DSLcontactus, name='DSLcontactus'),
]