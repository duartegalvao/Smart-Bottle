# Generated by Django 2.2 on 2019-04-15 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BottleReading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.IntegerField(default=150)),
                ('weight', models.IntegerField(default=150)),
            ],
        ),
    ]
