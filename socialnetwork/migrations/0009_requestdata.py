# Generated by Django 4.2 on 2023-11-17 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0008_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('farmer_name', models.CharField(max_length=160)),
                ('product_name', models.CharField(max_length=160)),
                ('expiry_date', models.DateField()),
                ('quantity', models.IntegerField()),
            ],
        ),
    ]
