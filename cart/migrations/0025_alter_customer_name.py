# Generated by Django 4.1.2 on 2022-10-19 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0024_alter_orderitem_amount_alter_orderitem_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(blank=True, default='New Customer', max_length=200, null=True),
        ),
    ]