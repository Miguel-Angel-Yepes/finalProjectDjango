# Generated by Django 5.0.3 on 2024-03-21 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='noname', max_length=50)),
                ('price', models.FloatField(default=0)),
                ('stock', models.IntegerField(default=0)),
                ('category', models.CharField(default='nocategory', max_length=150)),
                ('isdiscount', models.BooleanField(default=False)),
                ('discount', models.IntegerField(null=True)),
                ('state', models.CharField(default='ACTIVO', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=200)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
    ]