# Generated by Django 3.0.5 on 2024-03-19 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0011_remove_stock_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ecom.Seller'),
        ),
    ]
