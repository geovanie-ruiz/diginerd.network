# Generated by Django 3.1.1 on 2020-09-17 23:02

from django.db import migrations, models
import django.db.models.deletion
import django_enumfield.db.fields
import network.models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_article_published_on'),
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='article',
            name='article_type',
            field=django_enumfield.db.fields.EnumField(default=1, enum=network.models.ArticleType),
        ),
        migrations.AddField(
            model_name='article',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='series_articles', to='network.series'),
        ),
    ]
