# Generated by Django 4.2.1 on 2023-06-08 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_paymentinfo_order_payment_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.AddField(
            model_name='order',
            name='cart_items',
            field=models.ManyToManyField(to='store.cartitem'),
        ),
    ]
