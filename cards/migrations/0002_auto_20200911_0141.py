# Generated by Django 3.1.1 on 2020-09-11 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardart',
            name='card_art',
            field=models.ImageField(default='art/no-img.jpg', upload_to='art/card/'),
        ),
        migrations.AddField(
            model_name='releaseset',
            name='set_art',
            field=models.ImageField(default='art/no-img.jpg', upload_to='art/set/'),
        ),
    ]
