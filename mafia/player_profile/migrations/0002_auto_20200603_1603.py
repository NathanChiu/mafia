# Generated by Django 3.0.5 on 2020-06-03 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player_profile', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playerprofile',
            old_name='nums',
            new_name='skill_uses_remaining',
        ),
    ]
