# Generated by Django 3.1.3 on 2020-11-07 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20201107_0124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speedtest',
            name='type',
            field=models.IntegerField(choices=[(0, 'Test'), (1, 'Adhoc'), (2, 'Scheduled')], default=0),
        ),
        migrations.AlterField(
            model_name='testnode',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
