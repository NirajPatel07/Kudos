import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from organizations.models import Organization
from users.models import User
from kudos.models import Kudo

class Command(BaseCommand):
    help = 'Generate demo data for the kudos application'

    def handle(self, *args, **options):
        self.stdout.write('Creating demo data...')

        # Create organizations
        organizations = [
            {'name': 'Tech Innovators Inc.', 'description': 'A leading technology company'},
            {'name': 'Creative Solutions Ltd.', 'description': 'Design and marketing agency'},
            {'name': 'Global Dynamics Corp.', 'description': 'International consulting firm'},
        ]

        org_objects = []
        for org_data in organizations:
            org, created = Organization.objects.get_or_create(
                name=org_data['name'],
                defaults={'description': org_data['description']}
            )
            org_objects.append(org)
            if created:
                self.stdout.write(f'Created organization: {org.name}')

        # Create users
        users_data = [
            # Tech Innovators Inc.
            {'username': 'alice_dev', 'first_name': 'Alice', 'last_name': 'Johnson', 'email': 'alice@techinnovators.com', 'org_idx': 0},
            {'username': 'bob_pm', 'first_name': 'Bob', 'last_name': 'Smith', 'email': 'bob@techinnovators.com', 'org_idx': 0},
            {'username': 'charlie_design', 'first_name': 'Charlie', 'last_name': 'Brown', 'email': 'charlie@techinnovators.com', 'org_idx': 0},
            {'username': 'diana_qa', 'first_name': 'Diana', 'last_name': 'Wilson', 'email': 'diana@techinnovators.com', 'org_idx': 0},
            {'username': 'eve_dev', 'first_name': 'Eve', 'last_name': 'Davis', 'email': 'eve@techinnovators.com', 'org_idx': 0},
            
            # Creative Solutions Ltd.
            {'username': 'frank_creative', 'first_name': 'Frank', 'last_name': 'Miller', 'email': 'frank@creative.com', 'org_idx': 1},
            {'username': 'grace_marketing', 'first_name': 'Grace', 'last_name': 'Lee', 'email': 'grace@creative.com', 'org_idx': 1},
            {'username': 'henry_design', 'first_name': 'Henry', 'last_name': 'Taylor', 'email': 'henry@creative.com', 'org_idx': 1},
            {'username': 'iris_copy', 'first_name': 'Iris', 'last_name': 'Anderson', 'email': 'iris@creative.com', 'org_idx': 1},
            
            # Global Dynamics Corp.
            {'username': 'jack_consultant', 'first_name': 'Jack', 'last_name': 'White', 'email': 'jack@global.com', 'org_idx': 2},
            {'username': 'kate_analyst', 'first_name': 'Kate', 'last_name': 'Moore', 'email': 'kate@global.com', 'org_idx': 2},
            {'username': 'liam_strategy', 'first_name': 'Liam', 'last_name': 'Clark', 'email': 'liam@global.com', 'org_idx': 2},
        ]

        user_objects = []
        for user_data in users_data:
            org = org_objects[user_data['org_idx']]
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'email': user_data['email'],
                    'organization': org,
                    'kudos_available': random.randint(0, 3),
                }
            )
            if created:
                user.set_password('password123')  # Simple password for demo
                user.save()
                user_objects.append(user)
                self.stdout.write(f'Created user: {user.username}')

        # Generate random kudos
        kudo_messages = [
            "Great job on the project delivery!",
            "Thanks for helping me debug that tricky issue.",
            "Your presentation was fantastic!",
            "I appreciate your collaboration on the design.",
            "Amazing work on the client proposal!",
            "Thanks for staying late to meet the deadline.",
            "Your code review feedback was very helpful.",
            "Excellent problem-solving skills!",
            "Thanks for mentoring the new team member.",
            "Your creative ideas really made a difference.",
            "Great teamwork during the sprint!",
            "Thanks for the quick response to my questions.",
            "Your attention to detail is impressive.",
            "Thanks for organizing the team meeting.",
            "Wonderful job on the user interface design!",
            "Your testing caught some critical bugs.",
            "Thanks for the thorough documentation.",
            "Great communication with the client.",
            "Your efficiency is inspiring!",
            "Thanks for sharing your knowledge.",
        ]

        # Clear existing kudos to avoid duplicates in demo
        if self.confirm_action("Clear existing kudos? (y/N): "):
            Kudo.objects.all().delete()
            self.stdout.write('Cleared existing kudos')

        # Generate kudos within organizations
        kudos_created = 0
        for org in org_objects:
            org_users = [u for u in user_objects if u.organization == org]
            if len(org_users) < 2:
                continue
                
            # Generate random kudos between users in same organization
            for _ in range(random.randint(5, 15)):
                giver = random.choice(org_users)
                receiver = random.choice([u for u in org_users if u != giver])
                message = random.choice(kudo_messages)
                
                # Random time in the past week
                created_time = timezone.now() - timedelta(
                    days=random.randint(0, 7),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                
                kudo = Kudo.objects.create(
                    giver=giver,
                    receiver=receiver,
                    message=message,
                )
                # Manually set created_at to random time
                kudo.created_at = created_time
                kudo.save()
                kudos_created += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {kudos_created} kudos')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Demo data generation complete!')
        )
        self.stdout.write('You can now log in with any username and password "password123"')

    def confirm_action(self, message):
        """Ask user for confirmation"""
        response = input(message)
        return response.lower() in ['y', 'yes']
