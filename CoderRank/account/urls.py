from django.urls import path
from . import views


urlpatterns=[path('register',views.register,name='register'),
             path('profile/<str:username>',views.profile, name='profile'),
             path('login',views.user_login, name='login'),
             path('logout',views.user_logout, name='logout'),
             path('settings',views.edit_profile, name='edit_profile'),
             path('delete',views.delete_profile, name='delete_profile'),
             ]