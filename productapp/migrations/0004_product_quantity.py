# Generated by Django 4.2.6 on 2023-11-03 09:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("productapp", "0003_invoice_alter_product_product_name_product_invoice"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="quantity",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
