# Generated by Django 2.2.4 on 2019-08-11 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestApp', '0004_auto_20190810_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='descricao',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]
