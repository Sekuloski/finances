# Generated by Django 4.0.6 on 2022-07-19 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('State', '0020_alter_payment_fullpayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='testPayment',
            field=models.BooleanField(default=False),
        ),
    ]