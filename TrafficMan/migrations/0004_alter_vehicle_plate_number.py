# Generated by Django 3.2.3 on 2021-05-26 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrafficMan', '0003_alter_violationprocess_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='plate_number',
            field=models.CharField(max_length=20, null=True, unique=True, verbose_name='车牌号码'),
        ),
    ]
