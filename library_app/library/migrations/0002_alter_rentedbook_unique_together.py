# Generated by Django 4.0.4 on 2022-05-12 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rentedbook',
            unique_together=set(),
        ),
    ]
