from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
import telebot
import datetime
from .models import *


bot = telebot.TeleBot('6662564297:AAEEiCCDjKpTDy_C7t5eZP7tM9cCb861W94')
class HomePageView(View):
  def get(self, request):
    live_streams = YouTubeStreams.objects.all().order_by('?')[:15]
    return render(request, 'index.html', {'live_streams': live_streams})
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main:home')  
        else:
            message = "Invalid username or password."
            return render(request, 'login.html', {'message': message})
class RegisterView(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        username = request.POST.get('username')
        steam_id = request.POST.get('steam_id')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print(password , confirm_password)

        if User.objects.filter(username=username).exists():
            message = "Username already exists."
            return render(request, 'signup.html', {'message': message})
        elif Player.objects.filter(steam_id=steam_id).exists():
            message = "Steam ID already exists."
            return render(request, 'signup.html', {'message': message})
        elif password != confirm_password:
            message = "Passwords do not match."
            return render(request, 'signup.html', {'message': message})
        else:
            user = User.objects.create_user(username=username, password=password)
            player = Player.objects.create(user=user, steam_id=steam_id)
            player.save()
            user.save()
            return redirect('main:login')
class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
         return redirect('main:login')
        else:
         player = Player.objects.get(user=request.user)
         players_in_team = Player.objects.filter(team=request.user.player.team)
         user_notifications = Notifications.objects.filter(notifications=request.user.player.team).order_by('-id')[:4]
         context = {'player': player, 'players_in_team': players_in_team, 'notifications': user_notifications}
         return render(request, 'profile.html', context)
class YouTubeStreamsView(View):
    def get(self, request):
        top_streams = YouTubeStreams.objects.all().order_by('?')[:15]
        streams = YouTubeStreams.objects.all()[:15]
        return render(request, 'streams.html', {'streams': streams, 'top_streams': top_streams})

class AddPlayerView(View):
    
    def get(self, request):
     if not request.user.is_authenticated:
      return redirect('main:login')
     else:
      return render(request, 'add_player.html')

    def post(self, request):
        player = Player.objects.get(user=request.user)

        profile_id = request.POST.get('profile_id')

        try:
            new_player = Player.objects.get(profile_id=profile_id)
        except Player.DoesNotExist:
            return render(request, 'add_player.html', {'error': "Player not found."}) 

        team_players_count = Player.objects.filter(team=player.team).count()
        Notifications.objects.create(text=f"{new_player.user.username} joined your team!", notifications=player.team)
        if team_players_count >= 5:
            return render(request, 'add_player.html', {'error': "Team already has the maximum number of players."})

        new_player.team = player.team
        new_player.save()

        return redirect('main:profile')
    
class TournamentsView(View):
    def get(self, request):
        if not request.user.is_authenticated:
         return redirect('main:login')
        else:
         top_tournaments = Tournament.objects.all().order_by('?')[:6]
         tournaments = Tournament.objects.all()[:15]
         return render(request, 'turnirs.html', {'tournaments': tournaments, 'top_tournaments': top_tournaments})
class ParticipateView(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
         return redirect('main:login')
        else:
         tournament = Tournament.objects.get(id=pk)
         player = Player.objects.get(user=request.user)
         n = Notifications.objects.create(text=f"{player.team.team_id} joined {tournament.name}! ", notifications=player.team)
         n.save()
         bot.send_message('-1002033761247', f"""#Team_ID: {player.team.team_id} joined 
#Tournament_ID: {tournament.tournament_id}  """)

         return redirect('main:profile')