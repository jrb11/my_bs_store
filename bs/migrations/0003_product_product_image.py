# Generated by Django 4.0.5 on 2022-06-24 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bs', '0002_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Product_Image',
            field=models.ImageField(blank=True, null=True, upload_to='products'),
        ),
    ]
