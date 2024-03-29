# Generated by Django 4.0.6 on 2022-07-18 12:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('State', '0006_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='SixMonthPayment',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='State.payment')),
                ('monthsLeft', models.IntegerField(default=6)),
            ],
            bases=('State.payment',),
        ),
        migrations.CreateModel(
            name='ThreeMonthPayment',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='State.payment')),
                ('monthsLeft', models.IntegerField()),
            ],
            bases=('State.payment',),
        ),
        migrations.AddField(
            model_name='payment',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
