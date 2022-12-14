# Generated by Django 4.1.3 on 2022-11-17 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("class_name", models.CharField(max_length=300)),
                ("sender", models.CharField(max_length=50)),
                ("message", models.CharField(max_length=1000)),
                ("created_at", models.DateTimeField(verbose_name="created at")),
            ],
        ),
    ]
