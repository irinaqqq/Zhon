# Generated by Django 5.0.4 on 2024-04-22 21:50

import main.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_remove_custom_classroom_progress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=main.models.generate_filename2)),
            ],
        ),
        migrations.AddField(
            model_name='topic',
            name='images',
            field=models.ManyToManyField(blank=True, to='main.image'),
        ),
    ]
