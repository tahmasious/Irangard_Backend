# Generated by Django 3.2.8 on 2022-05-25 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0003_tour_bookers'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='total_revenue',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
    ]
