# Generated by Django 2.2.14 on 2021-04-01 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_trayek_trayek'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='activated',
            field=models.BooleanField(default=False),
        ),
    ]