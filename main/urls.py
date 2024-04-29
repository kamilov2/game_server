from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
 path('', HomePageView.as_view(), name='home'),
 path('login/', LoginView.as_view(), name='login'),
 path('register/', RegisterView.as_view(), name='register'),
 path('profile/', ProfileView.as_view(), name='profile'),
 path('streams/', YouTubeStreamsView.as_view(), name='streams'),
 path('add_player/', AddPlayerView.as_view(), name='add_player'),
 path('tournaments/', TournamentsView.as_view(), name='tournaments'),
 path('participate/<int:pk>/', ParticipateView.as_view(), name='participate'),
 path('logout/', LogoutView.as_view(), name='logout'),
]