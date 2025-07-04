from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from users.models import User

class Command(BaseCommand):
    help = 'Reset kudos for all users (run weekly)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force reset even if not a week since last reset',
        )

    def handle(self, *args, **options):
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        
        if options['force']:
            users_to_reset = User.objects.all()
            self.stdout.write('Force resetting kudos for all users...')
        else:
            users_to_reset = User.objects.filter(last_kudos_reset__lt=week_ago)
            self.stdout.write(f'Resetting kudos for users who haven\'t been reset in a week...')

        count = users_to_reset.count()
        users_to_reset.update(
            kudos_available=3,
            last_kudos_reset=now
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully reset kudos for {count} users')
        )
