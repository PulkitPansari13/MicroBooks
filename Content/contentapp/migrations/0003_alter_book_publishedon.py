# Generated by Django 4.0.1 on 2022-02-04 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contentapp', '0002_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publishedOn',
            field=models.DateField(),
        ),
    ]
