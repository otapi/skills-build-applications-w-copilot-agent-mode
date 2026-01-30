from djongo import models


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=24)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.email


class Team(models.Model):
    id = models.CharField(primary_key=True, max_length=24)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name


class Activity(models.Model):
    id = models.CharField(primary_key=True, max_length=24)
    user = models.ForeignKey(User, to_field='id', db_column='user_id', on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    duration = models.IntegerField()  # minutes
    date = models.DateField()
    def __str__(self):
        return f"{self.user.email} - {self.type}"


class Workout(models.Model):
    id = models.CharField(primary_key=True, max_length=24)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    suggested_for = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Leaderboard(models.Model):
    id = models.CharField(primary_key=True, max_length=24)
    team = models.ForeignKey(Team, to_field='id', db_column='team_id', on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.team.name} - {self.points}"
