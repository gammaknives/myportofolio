from django.db import migrations
from django.contrib.auth.hashers import make_password


def update_editor_password(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.filter(username="Editor").update(
        password=make_password("editing123editing")
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_seed_grader_account"),
    ]

    operations = [
        migrations.RunPython(update_editor_password, migrations.RunPython.noop),
    ]