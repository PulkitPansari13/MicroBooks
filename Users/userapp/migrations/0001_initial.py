# Generated by Django 4.0.1 on 2022-01-31 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=75)),
                ('last_name', models.CharField(max_length=75)),
                ('email_id', models.EmailField(max_length=254)),
                ('phno', models.CharField(max_length=10)),
            ],
        ),
    ]
