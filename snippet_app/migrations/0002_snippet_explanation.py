# Generated by Django 4.1 on 2023-02-25 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippet_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='explanation',
            field=models.TextField(blank=True, null=True),
        ),
    ]
