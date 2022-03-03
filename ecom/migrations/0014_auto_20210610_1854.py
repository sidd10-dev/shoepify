# Generated by Django 3.2 on 2021-06-10 13:24

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0013_alter_order_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone1',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None),
        ),
        migrations.AddField(
            model_name='customer',
            name='phone2',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None),
        ),
        migrations.AddField(
            model_name='customer',
            name='pincode',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.DeleteModel(
            name='PhoneNumber',
        ),
    ]