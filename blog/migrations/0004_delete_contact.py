# Generated by Django 4.2.7 on 2024-04-17 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_contact'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Contact',
        ),
    ]