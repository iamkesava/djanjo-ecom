# Generated by Django 3.0.5 on 2024-03-19 05:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecom', '0006_auto_20240317_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='product',
            name='cat',
            field=models.CharField(choices=[('Computer', 'Computer'), ('Projector', 'Projector'), ('Keyboard', 'Keyboard'), ('Mouse', 'Mouse')], max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=150)),
                ('address', models.CharField(max_length=150)),
                ('mobile', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]