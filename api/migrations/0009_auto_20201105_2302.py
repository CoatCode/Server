# Generated by Django 3.0.5 on 2020-11-05 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20201105_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.CharField(default='안녕하세요. <django.db.models.fields.CharField>입니다.', max_length=255),
        ),
    ]