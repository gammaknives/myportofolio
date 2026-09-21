from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_grader_account(apps, schema_editor):
    User = apps.get_model("auth", "User")
    if not User.objects.filter(username="burhan").exists():
        User.objects.create(
            username="burhan",
            password=make_password("burunghantu123"),
            is_staff=True,
            is_superuser=True,
        )


def remove_grader_account(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.filter(username="burhan").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_seed_initial_data"),
    ]

    operations = [
        migrations.RunPython(create_grader_account, remove_grader_account),
    ]