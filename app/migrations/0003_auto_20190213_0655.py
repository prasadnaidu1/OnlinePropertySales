# Generated by Django 2.1.7 on 2019-02-13 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_userregister_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userregister',
            name='id',
        ),
        migrations.AlterField(
            model_name='userregister',
            name='email',
            field=models.EmailField(max_length=254, primary_key=True, serialize=False),
        ),
    ]