# Generated by Django 4.2.3 on 2023-07-19 06:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0002_bond_delete_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bond',
            name='contract_data',
        ),
        migrations.RemoveField(
            model_name='bond',
            name='contract_expiration_data',
        ),
        migrations.RemoveField(
            model_name='bond',
            name='created',
        ),
        migrations.RemoveField(
            model_name='bond',
            name='interest',
        ),
        migrations.RemoveField(
            model_name='bond',
            name='interest_interval',
        ),
        migrations.AddField(
            model_name='bond',
            name='expiration_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='bond',
            name='interest_payment_frequency',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='bond',
            name='interest_rate',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='bond',
            name='purchase_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='bond',
            name='isin',
            field=models.CharField(max_length=12, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='bond',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='bond',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volume', models.PositiveIntegerField()),
                ('bond', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.bond')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]