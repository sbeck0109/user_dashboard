# Generated by Django 2.2 on 2020-09-05 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo_wall_app', '0005_user_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='level',
            field=models.CharField(max_length=45, null=True),
        ),
    ]