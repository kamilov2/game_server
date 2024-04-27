from django.db import models
from django.contrib.auth.models import User
import uuid

class Team(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=4)
    team_id = models.CharField(default=uuid.uuid4, editable=False, max_length=4) 
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()


    def __str__(self):
        return self.team_id

class Notifications(models.Model):
    notifications = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(blank=True)
    status = models.BooleanField(default=False)

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=4)  
    steam_id = models.CharField(max_length=100, blank=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.team: 
            self.team = Team.objects.create(name=f"{self.user.username}'s Team", description="Default team for player", team_id=uuid.uuid4()) 

        super(Player, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class YouTubeStreams(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'YouTube Stream'
        verbose_name_plural = 'YouTube Streams'

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="tournaments", blank=True)
    description = models.TextField(blank=True)
    tournament_id = models.CharField(default=uuid.uuid4, editable=False, max_length=4) 


    def __str__(self):
        return self.name