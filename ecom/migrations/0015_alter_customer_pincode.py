# Generated by Django 3.2 on 2021-06-10 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0014_auto_20210610_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='pincode',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
