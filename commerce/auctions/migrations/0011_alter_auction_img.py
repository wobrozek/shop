# Generated by Django 4.0.4 on 2023-02-27 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_auction_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='img',
            field=models.ImageField(blank='true', null='true', upload_to='auctions/files/auctionImg'),
        ),
    ]
