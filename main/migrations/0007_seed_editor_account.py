from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_editor_account(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Group = apps.get_model("auth", "Group")
    editor_group, _ = Group.objects.get_or_create(name="Editor")

    if not User.objects.filter(username="Editor").exists():
        editor_user = User.objects.create(
            username="Editor",
            password=make_password("editor123"),
            is_staff=True,
            is_superuser=False,
        )
        editor_user.groups.add(editor_group)


def remove_editor_account(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Group = apps.get_model("auth", "Group")

    User.objects.filter(username="Editor").delete()
    Group.objects.filter(name="Editor").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_seed_grader_account"),
    ]

    operations = [
        migrations.RunPython(create_editor_account, remove_editor_account),
    ]