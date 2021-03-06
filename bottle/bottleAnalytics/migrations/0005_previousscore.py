# Generated by Django 2.2 on 2019-05-03 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bottleAnalytics', '0004_auto_20190430_2039'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreviousScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calculated', models.DateTimeField(auto_now=True)),
                ('score', models.CharField(choices=[('A', 'Ideal hydration!'), ('B', 'Slightly lower than expected...'), ('C', 'Lower than expected...'), ('D', 'Too low hydration.'), ('E', 'No values available.'), ('O', 'Might be over-hydrating!')], default='E', max_length=1)),
            ],
        ),
    ]
