# Generated by Django 5.0.4 on 2024-04-20 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_payment_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entries',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/'),
        ),
    ]
