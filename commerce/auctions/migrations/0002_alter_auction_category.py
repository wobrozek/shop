# Generated by Django 4.0.4 on 2022-09-21 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.CharField(choices=[('FASHION', 'Fashion'), ('TOYS', 'Toys'), ('ELECTRONICS', 'Electronics'), ('HOME', 'Home'), ('CARS', 'Cars')], max_length=20),
        ),
    ]
