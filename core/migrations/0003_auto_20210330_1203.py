# Generated by Django 2.2.14 on 2021-03-30 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_seat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track1', models.CharField(max_length=15)),
                ('track2', models.CharField(max_length=15)),
                ('harga', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='bus',
            name='track1',
        ),
        migrations.RemoveField(
            model_name='bus',
            name='track2',
        ),
        migrations.AlterField(
            model_name='bus',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('tanggal', models.DateField()),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Track')),
            ],
        ),
    ]
