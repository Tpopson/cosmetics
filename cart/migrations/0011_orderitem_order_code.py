# Generated by Django 4.1.2 on 2022-10-19 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0010_alter_orderitem_amount_alter_orderitem_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='order_code',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
