# Generated by Django 2.1.7 on 2019-11-26 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publishers', '0026_auto_20191126_0525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publisher',
            name='description',
            field=models.CharField(max_length=150, null=True, verbose_name='description'),
        ),
    ]
