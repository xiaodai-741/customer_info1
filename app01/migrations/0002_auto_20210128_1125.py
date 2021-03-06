# Generated by Django 2.0 on 2021-01-28 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='saleman',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='saleman',
            name='hiredate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='saleman',
            name='home_address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='saleman',
            name='resignation_time',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='saleman',
            name='salary',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='boss_birthday',
            field=models.DateField(blank=True, null=True),
        ),
    ]
