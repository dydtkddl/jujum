# Generated by Django 4.1.6 on 2023-09-18 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0011_food_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="detail",
            field=models.TextField(null=True),
        ),
    ]
