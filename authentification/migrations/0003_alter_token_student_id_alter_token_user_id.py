# Generated by Django 4.1.3 on 2022-11-17 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0002_token_student_id_token_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='student_id',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='user_id',
            field=models.CharField(max_length=10, null=True),
        ),
    ]