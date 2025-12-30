from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'


    def handle(self, *args, **kwargs):

        # Workaround: Use raw pymongo to insert test data directly
        from django.conf import settings
        from pymongo import MongoClient
        from bson import ObjectId
        import datetime

        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'], settings.DATABASES['default']['CLIENT']['port'])
        db = client[settings.DATABASES['default']['NAME']]

        db['activities'].drop()
        db['leaderboard'].drop()
        db['workouts'].drop()
        db['users'].drop()
        db['teams'].drop()

        # Insert Teams
        marvel_id = ObjectId()
        dc_id = ObjectId()
        db['teams'].insert_many([
            {'_id': marvel_id, 'name': 'Marvel'},
            {'_id': dc_id, 'name': 'DC'}
        ])

        # Insert Users
        tony_id = ObjectId()
        steve_id = ObjectId()
        bruce_id = ObjectId()
        clark_id = ObjectId()
        db['users'].insert_many([
            {'_id': tony_id, 'name': 'Tony Stark', 'email': 'tony@marvel.com', 'team_id': marvel_id},
            {'_id': steve_id, 'name': 'Steve Rogers', 'email': 'steve@marvel.com', 'team_id': marvel_id},
            {'_id': bruce_id, 'name': 'Bruce Wayne', 'email': 'bruce@dc.com', 'team_id': dc_id},
            {'_id': clark_id, 'name': 'Clark Kent', 'email': 'clark@dc.com', 'team_id': dc_id},
        ])

        # Insert Activities
        today = datetime.datetime.utcnow().date()
        db['activities'].insert_many([
            {'user_id': tony_id, 'type': 'Run', 'duration': 30, 'date': str(today)},
            {'user_id': steve_id, 'type': 'Swim', 'duration': 45, 'date': str(today)},
            {'user_id': bruce_id, 'type': 'Cycle', 'duration': 60, 'date': str(today)},
            {'user_id': clark_id, 'type': 'Yoga', 'duration': 20, 'date': str(today)},
        ])

        # Insert Workouts
        w1_id = ObjectId()
        w2_id = ObjectId()
        db['workouts'].insert_many([
            {'_id': w1_id, 'name': 'Pushups', 'description': 'Do 20 pushups', 'suggested_for': [tony_id, bruce_id]},
            {'_id': w2_id, 'name': 'Situps', 'description': 'Do 30 situps', 'suggested_for': [steve_id, clark_id]},
        ])

        # Insert Leaderboard
        db['leaderboard'].insert_many([
            {'team_id': marvel_id, 'score': 150},
            {'team_id': dc_id, 'score': 120},
        ])

        self.stdout.write(self.style.SUCCESS('Database populated with test data using raw pymongo.'))

        # Create Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create Users
        tony = User.objects.create(name='Tony Stark', email='tony@marvel.com', team=marvel)
        steve = User.objects.create(name='Steve Rogers', email='steve@marvel.com', team=marvel)
        bruce = User.objects.create(name='Bruce Wayne', email='bruce@dc.com', team=dc)
        clark = User.objects.create(name='Clark Kent', email='clark@dc.com', team=dc)

        # Create Activities
        Activity.objects.create(user=tony, type='Run', duration=30, date=timezone.now().date())
        Activity.objects.create(user=steve, type='Swim', duration=45, date=timezone.now().date())
        Activity.objects.create(user=bruce, type='Cycle', duration=60, date=timezone.now().date())
        Activity.objects.create(user=clark, type='Yoga', duration=20, date=timezone.now().date())

        # Create Workouts
        w1 = Workout.objects.create(name='Pushups', description='Do 20 pushups')
        w2 = Workout.objects.create(name='Situps', description='Do 30 situps')
        w1.suggested_for.set([tony, bruce])
        w2.suggested_for.set([steve, clark])

        # Create Leaderboard
        Leaderboard.objects.create(team=marvel, score=150)
        Leaderboard.objects.create(team=dc, score=120)

        self.stdout.write(self.style.SUCCESS('Database populated with test data.'))
