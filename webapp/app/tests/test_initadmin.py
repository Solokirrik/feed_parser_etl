import os
import pytest
from django.contrib.auth.models import User
from app.management.commands.initadmin import Command


@pytest.mark.django_db
def test_handle():
    Command().handle()
    username = os.getenv('DJANGO_SU_NAME')
    user = User.objects.filter(username=username)
    assert all(prop for prop in [user.exists(),
                                 user.get().is_active,
                                 user.get().is_staff,
                                 user.get().is_superuser])
