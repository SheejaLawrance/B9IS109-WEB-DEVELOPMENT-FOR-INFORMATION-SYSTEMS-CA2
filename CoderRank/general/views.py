from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from account.models import Profile
# Create your views here.

def home(request):
    
    return render(request,"home.html")
   