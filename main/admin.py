from django.contrib import admin
from .models import Team, Notifications, Player, YouTubeStreams, Tournament

class TeamAdmin(admin.ModelAdmin):
    search_fields = ['id', 'team_id', 'name', 'description']

class NotificationsAdmin(admin.ModelAdmin):
    search_fields = ['notifications__name', 'text']



class YouTubeStreamsAdmin(admin.ModelAdmin):
    search_fields = ['name', 'link', 'description']

class TournamentAdmin(admin.ModelAdmin):
    search_fields = ['name', 'tournament_id', 'description']

admin.site.register(Team, TeamAdmin)
admin.site.register(Notifications, NotificationsAdmin)
admin.site.register(YouTubeStreams, YouTubeStreamsAdmin)
admin.site.register(Tournament, TournamentAdmin)
