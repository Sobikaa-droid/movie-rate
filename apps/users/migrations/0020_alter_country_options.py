# Generated by Django 5.0.6 on 2024-07-27 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_alter_country_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ['common_name']},
        ),
    ]
