# Generated by Django 3.1.2 on 2020-10-24 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0015_auto_20201022_0237'),
    ]

    operations = [
        migrations.AddField(
            model_name='digivolvecost',
            name='level',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='digivolvecost',
            name='cost',
            field=models.IntegerField(),
        ),
    ]
