# Generated by Django 3.2.12 on 2022-02-09 14:52

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deviceMac', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default=core.models.key_generator, editable=False, max_length=24, unique=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('expired_on', models.DateField()),
                ('deviceNumber', models.IntegerField(default=1)),
                ('licenseType', models.CharField(choices=[('trial', 'Trial'), ('time limit', 'Time Limit')], max_length=255)),
                ('email', models.EmailField(max_length=255, null=True)),
                ('serialNumber', models.CharField(default=core.models.create_new_ref_number, editable=False, max_length=255, unique=True)),
                ('devices', models.ManyToManyField(blank=True, related_name='devices', to='core.Device')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone_number', models.CharField(max_length=11, unique=True, validators=[core.models.validate_phone_number])),
                ('name', models.CharField(max_length=255, null=True)),
                ('generated_token', models.IntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]