# Generated by Django 3.2.3 on 2021-05-31 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TrafficMan', '0006_violationprocessrecordview'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(verbose_name='登记时间')),
                ('is_finished', models.BooleanField(verbose_name='是否完成')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TrafficMan.userprofile', verbose_name='驾驶员')),
            ],
            options={
                'verbose_name': '道路安全学习信息管理',
                'verbose_name_plural': '道路安全学习信息管理',
            },
        ),
        migrations.AlterModelOptions(
            name='violationprocess',
            options={'verbose_name': '违章处理记录管理', 'verbose_name_plural': '违章处理记录管理'},
        ),
        migrations.CreateModel(
            name='EducationRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finish_time', models.DateTimeField(verbose_name='学习完成时间')),
                ('education', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='TrafficMan.education', verbose_name='学习ID')),
            ],
            options={
                'verbose_name': '道路安全学习记录管理',
                'verbose_name_plural': '道路安全学习记录管理',
            },
        ),
    ]