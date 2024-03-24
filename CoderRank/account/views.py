from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Profile 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from quiz.models import QuizSubmission


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
    #show results on profile
    result=QuizSubmission.objects.filter(user=user_obj)
    
    
    context={"user_profile":user_profile, "result":result}
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
    user_obj=User.objects.get(username=request.user)
    user_profile=Profile.objects.get(user=user_obj)
    
    if request.method=="POST":
        #img
        if request.FILES.get('profile_img')!=None:
            user_profile.profile_img=request.FILES.get('profile_img')
            user_profile.save()
        
        #email    
        if request.POST.get('email')!=None:
            u=User.objects.filter(email=request.POST.get('email')).first()
            
            if u==None:
                user_obj.email=request.POST.get('email')
                user_obj.save()
            else:
                if u!=user_obj:
                    messages.info(request,"This email id registered with another user, Try a different one!")
                    return redirect('edit_profile')
                
            
        #username
        if request.POST.get('username')!=None:
            u=User.objects.filter(username=request.POST.get('username')).first()
            
            if u==None:
                user_obj.username=request.POST.get('username')
                user_obj.save()
            else:
                if u!=user_obj:
                    messages.info(request,"This username is registered with another user, Try a different one!")
                    return redirect('edit_profile')
                
        #fname and lname
        user_obj.first_name=request.POST.get('firstname')
        user_obj.last_name=request.POST.get('lastname')
        user_obj.save()
        
        #location
        user_profile.location=request.POST.get('location')
        #experience
        user_profile.years_of_exp=request.POST.get('experience')
        #education
        user_profile.education=request.POST.get('education')
        #bio
        user_profile.bio=request.POST.get('bio')
        #job
        user_profile.job_title=request.POST.get('jobtitle')
        
        user_profile.save()
        
        return redirect('profile', user_obj.username)
            
    context={"user_profile":user_profile}
    return render(request,'edit_profile.html',context)

@login_required(login_url='login')
def delete_profile(request):
    user_obj=User.objects.get(username=request.user)
    user_profile=Profile.objects.get(user=user_obj)
    
    if request.method=="POST":
        #profile delete
        user_profile.delete()
        #user delete
        user_obj.delete()
        #logout
        return redirect('logout')
        
        
    
    context={"user_profile":user_profile}
    return render(request,'confirm_profile.html',context)
