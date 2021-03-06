# Generated by Django 4.0.5 on 2022-06-24 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('Create_Date', models.DateField(auto_created=True, null=True)),
                ('Product_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Product_Name', models.CharField(max_length=20, null=True)),
                ('IS_Deleted', models.BooleanField()),
                ('Created_By_User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bs.user_details')),
            ],
        ),
    ]
