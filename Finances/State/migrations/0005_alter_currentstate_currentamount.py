# Generated by Django 4.0.6 on 2022-07-18 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('State', '0004_currentstate_currentamount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentstate',
            name='currentAmount',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
