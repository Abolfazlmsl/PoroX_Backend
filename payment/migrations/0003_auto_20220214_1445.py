# Generated by Django 3.2.12 on 2022-02-14 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_rename_main_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='deviceNumber',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='payment',
            name='email',
            field=models.EmailField(default=0, max_length=255),
        ),
        migrations.AddField(
            model_name='payment',
            name='name',
            field=models.TextField(default=0),
        ),
        migrations.AddField(
            model_name='payment',
            name='phone',
            field=models.CharField(default=0, max_length=11),
        ),
        migrations.AddField(
            model_name='payment',
            name='time',
            field=models.DateField(null=True),
        ),
    ]