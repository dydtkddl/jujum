# Generated by Django 3.2.19 on 2023-09-20 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20230920_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='eachorder',
            name='servedTime',
            field=models.DateTimeField(null=True),
        ),
    ]