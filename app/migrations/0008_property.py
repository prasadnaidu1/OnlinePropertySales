# Generated by Django 2.1.7 on 2019-02-13 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20190213_0848'),
    ]

    operations = [
        migrations.CreateModel(
            name='property',
            fields=[
                ('property_id', models.AutoField(primary_key=True, serialize=False)),
                ('property_name', models.CharField(max_length=20)),
            ],
        ),
    ]