# Generated by Django 4.0.1 on 2022-02-01 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interactionapp.book')),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interactionapp.user')),
            ],
            options={
                'unique_together': {('userID', 'bookID')},
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interactionapp.book')),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interactionapp.user')),
            ],
            options={
                'unique_together': {('userID', 'bookID')},
            },
        ),
    ]