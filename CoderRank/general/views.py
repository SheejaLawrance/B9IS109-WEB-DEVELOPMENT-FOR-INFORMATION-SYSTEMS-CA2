from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from account.models import Profile
from quiz.models import UserRank
from django.contrib.auth.decorators import login_required
# Create your views here.



def home(request):
    
    leaderboard_users=UserRank.objects.order_by('rank')[:3]
    print(leaderboard_users)
    if request.user.is_authenticated:
        user_obj=User.objects.get(username=request.user)
        user_profile=Profile.objects.get(user=user_obj)
        context={"leaderboard_users":leaderboard_users, "user_profile":user_profile}
        
    else:
        context={}
        
    return render(request,"home.html",context)
  
def about_us(request):
    return render(request, "about.html")

def faq(request):
    return render(request, "faq.html")

def contact(request):
    return render(request, "contact.html")