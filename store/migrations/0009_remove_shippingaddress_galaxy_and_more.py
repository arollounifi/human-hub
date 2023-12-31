# Generated by Django 4.2.1 on 2023-06-07 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_shippingaddress_order_order_shipping_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='galaxy',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='planet',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='solar_system',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='street_address',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='user',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='country',
            field=models.CharField(default='Default Value', max_length=100),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='postal_code',
            field=models.CharField(default='Default Value', max_length=20),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='state',
            field=models.CharField(default='Default Value', max_length=100),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='street',
            field=models.CharField(default='Default Value', max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.shippingaddress'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='city',
            field=models.CharField(default='Default Value', max_length=100),
        ),
    ]
