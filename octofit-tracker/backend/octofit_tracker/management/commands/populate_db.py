
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from uuid import uuid4

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):

        # Clear existing data using Djongo's raw MongoDB access
        from django.db import connection
        db = connection.cursor().db_conn.client['octofit_db']
        db.activity.delete_many({})
        db.leaderboard.delete_many({})
        db.workout.delete_many({})
        db.user.delete_many({})
        db.team.delete_many({})


        # Create teams with string IDs
        marvel = Team.objects.create(id=uuid4().hex, name='marvel', description='Marvel Team')
        dc = Team.objects.create(id=uuid4().hex, name='dc', description='DC Team')

        # Create users with string IDs
        users = [
            User(id=uuid4().hex, email='ironman@marvel.com', name='Iron Man', team='marvel'),
            User(id=uuid4().hex, email='captain@marvel.com', name='Captain America', team='marvel'),
            User(id=uuid4().hex, email='spiderman@marvel.com', name='Spider-Man', team='marvel'),
            User(id=uuid4().hex, email='batman@dc.com', name='Batman', team='dc'),
            User(id=uuid4().hex, email='superman@dc.com', name='Superman', team='dc'),
            User(id=uuid4().hex, email='wonderwoman@dc.com', name='Wonder Woman', team='dc'),
        ]
        for user in users:
            user.save()

        # Create activities with string IDs
        Activity.objects.create(id=uuid4().hex, user=users[0], type='run', duration=30, date=timezone.now())
        Activity.objects.create(id=uuid4().hex, user=users[1], type='walk', duration=60, date=timezone.now())
        Activity.objects.create(id=uuid4().hex, user=users[3], type='strength', duration=45, date=timezone.now())

        # Create workouts with string IDs
        Workout.objects.create(id=uuid4().hex, name='Pushups', description='Do 20 pushups', suggested_for='marvel')
        Workout.objects.create(id=uuid4().hex, name='Situps', description='Do 30 situps', suggested_for='dc')

        # Create leaderboard with string IDs
        Leaderboard.objects.create(id=uuid4().hex, team=marvel, points=150)
        Leaderboard.objects.create(id=uuid4().hex, team=dc, points=120)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
