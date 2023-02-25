# Generated by Django 4.1 on 2023-02-25 04:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snippet_app', '0003_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='lang',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='snippet_app.user'),
            preserve_default=False,
        ),
    ]
