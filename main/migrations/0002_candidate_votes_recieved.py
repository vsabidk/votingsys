# Generated by Django 4.1.5 on 2024-06-11 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="candidate",
            name="votes_Recieved",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
