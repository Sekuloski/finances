# Generated by Django 4.0.6 on 2022-07-18 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('State', '0011_alter_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threemonthpayment',
            name='monthsLeft',
            field=models.IntegerField(default=3),
        ),
    ]