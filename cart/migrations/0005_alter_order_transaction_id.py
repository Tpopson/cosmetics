# Generated by Django 4.1.2 on 2022-10-18 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_customer_device'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]