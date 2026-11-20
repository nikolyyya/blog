from django.conf import settings
from django.db import migrations


def add_missing_profiles(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    user = apps.get_model(app_label, model_name)
    profile = apps.get_model("accounts", "Profile")
    alias = schema_editor.connection.alias
    existing_ids = profile.objects.using(alias).values("user_id")
    missing_ids = user.objects.using(alias).exclude(pk__in=existing_ids).values_list("pk", flat=True)
    for user_id in missing_ids.iterator():
        profile.objects.using(alias).get_or_create(user_id=user_id)


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_missing_profiles, migrations.RunPython.noop),
    ]
