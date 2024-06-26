# Generated by Django 5.0.6 on 2024-06-19 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=350)),
                ('year', models.IntegerField()),
                ('genre', models.JSONField()),
                ('rating', models.DecimalField(decimal_places=2, max_digits=10)),
                ('director', models.CharField(max_length=150)),
                ('actors', models.JSONField()),
                ('plot', models.TextField(max_length=9999)),
                ('poster', models.URLField()),
                ('runtime', models.IntegerField()),
                ('country', models.CharField(max_length=100)),
                ('production', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
    ]