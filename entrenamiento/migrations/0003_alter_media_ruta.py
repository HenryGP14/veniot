# Generated by Django 3.2.14 on 2022-09-05 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entrenamiento', '0002_media_ruta_audio_clonado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='ruta',
            field=models.FileField(null=True, upload_to='sounds/'),
        ),
    ]
