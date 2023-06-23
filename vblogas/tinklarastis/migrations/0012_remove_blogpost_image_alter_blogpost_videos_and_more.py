# Generated by Django 4.2.2 on 2023-06-22 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinklarastis', '0011_remove_blogpost_video_blogpost_videos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='image',
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='videos',
            field=models.ManyToManyField(blank=True, null=True, to='tinklarastis.video'),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='image',
            field=models.ManyToManyField(blank=True, null=True, to='tinklarastis.image'),
        ),
    ]
