# Generated by Django 4.1.6 on 2023-09-18 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_users_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="users",
            name="isSuperViser",
            field=models.IntegerField(null=True),
        ),
    ]