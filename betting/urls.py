from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('profile', views.profile, name='profile'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('matches', views.matches, name='matches'),
    path('bett_match', views.bett_match, name='bett_match')
]