# Generated by Django 4.1.7 on 2023-06-22 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarousalImg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]