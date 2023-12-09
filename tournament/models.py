from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Team(models.Model):
    title = models.CharField(max_length=100)
    captain = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True, related_name='captain_teams')
    description = models.TextField()
    members = models.ManyToManyField(Player, related_name='teams')

    def __str__(self):
        return self.title


class Tournament(models.Model):
    title = models.CharField(max_length=100)
    slots = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    winning_prize = models.CharField(max_length=100)
    details = models.TextField()
    image = models.ImageField(
        upload_to='tournament_images/', null=True, blank=True)
    creator = models.ForeignKey(
        'Player', on_delete=models.SET_NULL, null=True, related_name='created_tournaments')

    def __str__(self):
        return self.title


class Match(models.Model):
    name = models.CharField(max_length=100)
    team1 = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='team1_matches')
    team2 = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='team2_matches')
    # Assuming this is a text field for spectators
    spectator = models.TextField(blank=True, null=True)
    time = models.DateTimeField()
    match_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}: {self.team1} vs {self.team2}"


class TournamentResult(models.Model):
    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name='results')
    winner = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, related_name='won_tournaments')
    match = models.ForeignKey(
        Match, on_delete=models.CASCADE, related_name='tournament_results')

    def __str__(self):
        return f"Results for {self.tournament}"
