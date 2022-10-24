# Generated by Django 4.1.2 on 2022-10-19 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_alter_orderitem_order_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='transaction_id',
        ),
        migrations.AddField(
            model_name='order',
            name='payment_code',
            field=models.CharField(blank=True, max_length=36, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='transaction_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]