# Generated by Django 4.0.4 on 2022-09-21 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_alter_auction_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.CharField(choices=[('FA', 'FASHION'), ('TO', 'TOYS'), ('EL', 'ELECTRONICS'), ('HO', 'HOME'), ('CR', 'CARS')], max_length=2),
        ),
    ]
