from django.shortcuts import render,redirect
from .models import Player, Match
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
import pandas as pd
from sqlalchemy import create_engine    
# Create your views here.

def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'Credentials Ivalid')
            return redirect('index')
    elif request.user.is_authenticated:

        return redirect('profile')
    else:
        return render(request, 'index.html')


def profile(request):
    players = Player.objects.all()



    # DEFINE THE DATABASE CREDENTIALS
    user="adrian"
    password=""
    host="localhost"
    port="5432"
    database="betting_app"
    
    # PYTHON FUNCTION TO CONNECT TO THE POSTGRESQL DATABASE AND
    # RETURN THE SQLACHEMY ENGINE OBJECT
    def get_connection():
        return create_engine(
            url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
                user, password, host, port, database
            )
        )

    engine = get_connection()
    df = pd.read_sql_query('select * from betting_player ORDER BY points DESC', con=engine)
    df_dict= {}
    for ind in df.index:
        df_dict[df['name'][ind]]=df['points'][ind]
    return render(request, 'profile.html', {'players': players,'df_dict': df_dict})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,first_name=first_name, last_name=last_name, email=email, password=password)
                user.save()
                Player.objects.create(name=username)
                return redirect('index')
        else:
            messages.info(request, 'Password Not The Same')
            return redirect('register')
    else:    
        return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def matches(request):
    matches = Match.objects.all()
    return render(request, 'matches.html', {'matches': matches})

def bett_match(request):
    matches = Match.objects.all()
    first_team_score =  request.POST.get('first_team_score')
    second_team_score = request.POST.get('second_team_score')

    return render(request, 'bett_match.html',{'matches': matches})
