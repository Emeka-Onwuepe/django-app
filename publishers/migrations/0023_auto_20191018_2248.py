# Generated by Django 2.1.7 on 2019-10-18 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publishers', '0022_auto_20191018_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='description',
            field=models.CharField(default='null', max_length=255),
        ),
    ]