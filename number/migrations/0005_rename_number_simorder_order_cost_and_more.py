# Generated by Django 4.0.3 on 2022-04-13 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('number', '0004_simorder_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='simorder',
            old_name='number',
            new_name='order_cost',
        ),
        migrations.AddField(
            model_name='simorder',
            name='order_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='simorder',
            name='tel_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]