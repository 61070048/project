# Generated by Django 3.0.3 on 2020-03-05 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20200228_2330'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='evet_date',
            new_name='event_date',
        ),
    ]