# Generated by Django 4.1 on 2023-02-25 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippet_app', '0002_snippet_explanation'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
            ],
        ),
    ]