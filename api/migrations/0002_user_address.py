# Generated by Django 4.1.1 on 2022-09-09 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(default='address', max_length=200),
            preserve_default=False,
        ),
    ]
