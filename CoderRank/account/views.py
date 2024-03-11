from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required



# Create your views here.

def register(request):
    
    if request.user.is_authenticated:
        return redirect('profile', request.user.username)
    
    if request.method=='POST':
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        password1=request.POST['password1']
        
        if password==password1:
        
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already registered. Try logging in")
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,"Username already taken")
                return redirect('register')
            else:
                #user creation
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                
                #login and redirect to profile
                user_login=authenticate(username=username,password=password)
                login(request, user_login)
                
                #profile creation
                user_model=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_model,email_id=email)
                new_profile.save()
                return redirect('profile',  username)
            
        else:
            messages.info(request,"Password not matching")
            return redirect('register')
    context={}
    return render(request,'register.html',context)

@login_required(login_url='login')
def profile(request,username):
    
    user_obj=User.objects.get(username=username)
    user_profile=Profile.objects.get(user=user_obj)
    
    context={"user_profile":user_profile}
    return render(request,"profile.html",context)

def user_login(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.username)
    
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        
        user_profile=authenticate(username=username, password=password)
        
        if user_profile is not None:
        
            login(request, user_profile)
            return redirect('profile',username)
        else:
            messages.info(request,'Invalid!')
            return redirect('login')
    
    return render(request,"login.html")


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def edit_profile(request):
    context={}
    return render(request,'edit_profile.html',context)

@login_required(login_url='login')
def delete_profile(request):
    context={}
    return render(request,'confirm_profile.html',context)
