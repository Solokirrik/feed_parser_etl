import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username, password = os.getenv('DJANGO_SU_NAME'), os.getenv('DJANGO_SU_PASS')
            email = os.getenv('DJANGO_SU_EMAIL')
            print('Creating user for %s (%s)' % (username, email))
            admin = User.objects.create_superuser(email=email, username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin user can only be initialized if no Users exist')
