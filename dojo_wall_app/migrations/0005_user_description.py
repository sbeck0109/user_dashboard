# Generated by Django 2.2 on 2020-09-05 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo_wall_app', '0004_user_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
