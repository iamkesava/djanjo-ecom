# Generated by Django 3.0.5 on 2024-03-19 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0012_orders_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='user_id',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
