# Generated by Django 4.1.3 on 2023-03-02 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_alter_auction_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='img',
            field=models.ImageField(upload_to='auctionImg/'),
        ),
    ]
