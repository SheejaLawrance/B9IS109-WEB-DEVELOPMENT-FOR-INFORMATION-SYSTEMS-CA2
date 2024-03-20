from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from account.models import Profile
from .models import Quiz, Category
from django.db.models import Q

# Create your views here.
@login_required(login_url='login')
def all_quiz_view(request):
    
    user_obj=User.objects.get(username=request.user)
    user_profile=Profile.objects.get(user=user_obj)
    
    quizzes=Quiz.objects.order_by('-created_at')
    categories=Category.objects.all()
    
    context={"user_profile":user_profile, "quizzes":quizzes, "categories":categories}
    return render(request,'quiz.html', context)
    
@login_required(login_url='login')    
def search_view(request, category):
    user_obj=User.objects.get(username=request.user)
    user_profile=Profile.objects.get(user=user_obj)
    
    #searchbar
    if request.GET.get('searchterm')!=None:
        searchterm=request.GET.get('searchterm')
        q=Q(title__icontains=searchterm) | Q(description__icontains=searchterm)
        quizzes=Quiz.objects.filter(q).distinct().order_by('-created_at')
        
    #filter
    elif category!=" ":
        quizzes=Quiz.objects.filter(category__name=category).order_by('-created_at')
    
    #all
    else:
        quizzes=Quiz.objects.order_by('-created_at')
        
    categories=Category.objects.all()
    
    context={"user_profile":user_profile, "quizzes":quizzes, "categories":categories}
    return render(request,'quiz.html', context)

@login_required(login_url='login')  
def quiz_view(request, quiz_id):
    
    user_obj=User.objects.get(username=request.user)
    user_profile=Profile.objects.get(user=user_obj)
    
    quiz=Quiz.objects.filter(id=quiz_id).first()
    if request.method=="POST":
        pass
    
    if quiz!=None:
        context={"user_profile":user_profile, "quiz":quiz}
        
    else:
        return redirect('all_quiz')

    return render(request,'mcq.html', context)