# Generated by Django 5.0.2 on 2024-04-18 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UIAsset', '0002_remove_tag_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
