# Generated by Django 4.0.6 on 2022-07-19 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('State', '0018_currentstate_totalsubscriptions'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='fullPayment',
            field=models.BooleanField(default=False),
        ),
    ]