# Generated by Django 4.2.9 on 2024-02-03 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_purchase_total_amount_alter_sale_total_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(blank=True, max_length=50)),
                ('customer_mobile', models.CharField(max_length=50)),
                ('customer_address', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='sale',
            name='customer_address',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='customer_mobile',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='customer_name',
        ),
        migrations.AddField(
            model_name='sale',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.customer'),
        ),
    ]
