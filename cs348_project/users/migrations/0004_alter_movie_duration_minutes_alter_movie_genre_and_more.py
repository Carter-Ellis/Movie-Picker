# Generated by Django 5.1.7 on 2025-04-15 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_movie_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='duration_minutes',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.TextField(db_index=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.TextField(db_index=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.IntegerField(db_index=True),
        ),
    ]
