# Generated by Django 3.2.3 on 2021-05-26 10:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TrafficMan', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExceededViolationView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='违章时间')),
                ('area', models.CharField(max_length=50, verbose_name='区域')),
                ('type', models.CharField(max_length=100, verbose_name='违章类型')),
                ('deadline', models.DateField(verbose_name='罚款缴纳截至日期')),
                ('fine', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='罚款')),
                ('plate_number', models.CharField(max_length=20, verbose_name='车牌号码')),
                ('driver_id', models.CharField(max_length=25, verbose_name='驾驶员身份证号')),
                ('driver_name', models.CharField(max_length=80, verbose_name='驾驶员姓名')),
                ('owner_id', models.CharField(max_length=25, verbose_name='车主身份证号')),
                ('owner_name', models.CharField(max_length=80, verbose_name='车主姓名')),
                ('is_processed', models.BooleanField(verbose_name='是否缴纳')),
            ],
            options={
                'verbose_name': '逾期违章查询',
                'verbose_name_plural': '逾期违章查询',
                'db_table': 'v_exceededviolation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OwnerVehicleView',
            fields=[
                ('identity', models.CharField(max_length=25, verbose_name='车主身份证号')),
                ('name', models.CharField(max_length=80, verbose_name='车主姓名')),
                ('gender', models.CharField(choices=[('M', '男'), ('F', '女')], max_length=5, verbose_name='性别')),
                ('ethnicity', models.CharField(max_length=20, verbose_name='民族')),
                ('nationality', models.CharField(max_length=10, verbose_name='国籍')),
                ('address', models.CharField(max_length=200, verbose_name='住址')),
                ('telephone', models.CharField(max_length=15, verbose_name='固定电话')),
                ('mobile', models.CharField(max_length=25, verbose_name='手机号码')),
                ('birth', models.DateField(verbose_name='出生日期')),
                ('engine_id', models.CharField(max_length=25, primary_key=True, serialize=False, verbose_name='机动车VIN编号')),
                ('brand', models.CharField(max_length=25, verbose_name='品牌')),
                ('manufacture_model', models.CharField(max_length=35, verbose_name='型号')),
                ('color', models.CharField(max_length=20, verbose_name='颜色')),
                ('vehicle_type', models.CharField(choices=[('A', '载货汽车'), ('B', '越野汽车'), ('C', '自卸汽车'), ('D', '牵引车'), ('E', '专用汽车'), ('F', '客车'), ('G', '轿车'), ('H', '半挂车'), ('K', '其它')], max_length=2, verbose_name='车型')),
                ('displacement', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='排量')),
                ('manufacture_date', models.DateField(verbose_name='出厂日期')),
                ('life_duration', models.PositiveIntegerField(verbose_name='使用年限（年）')),
                ('plate_number', models.CharField(max_length=20, verbose_name='车牌号码')),
                ('status', models.CharField(choices=[('A', 'A-正常'), ('B', 'B-转出'), ('C', 'C-被盗抢'), ('D', 'D-停驶'), ('E', 'E-注销'), ('G', 'F-违法未处理'), ('H', 'H-海关监管'), ('I', 'I-事故未处理'), ('J', 'J-嫌疑车'), ('K', 'K-查封'), ('L', 'L-暂扣'), ('M', 'M-强制注销'), ('N', 'N-事故逃逸'), ('O', 'O-锁定'), ('F', 'F-退车')], default='A', max_length=8, verbose_name='机动车状态')),
            ],
            options={
                'verbose_name': '机动车-车主信息联合查询',
                'verbose_name_plural': '机动车-车主信息联合查询',
                'db_table': 'v_vehicleowner',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UnprocessedViolationView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='违章时间')),
                ('area', models.CharField(max_length=50, verbose_name='区域')),
                ('type', models.CharField(max_length=100, verbose_name='违章类型')),
                ('deadline', models.DateField(verbose_name='罚款缴纳截至日期')),
                ('fine', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='罚款')),
                ('plate_number', models.CharField(max_length=20, verbose_name='车牌号码')),
                ('driver_id', models.CharField(max_length=25, verbose_name='驾驶员身份证号')),
                ('driver_name', models.CharField(max_length=80, verbose_name='驾驶员姓名')),
                ('owner_id', models.CharField(max_length=25, verbose_name='车主身份证号')),
                ('owner_name', models.CharField(max_length=80, verbose_name='车主姓名')),
                ('is_processed', models.BooleanField(verbose_name='是否缴纳')),
            ],
            options={
                'verbose_name': '未处理违章查询',
                'verbose_name_plural': '未处理违章查询',
                'db_table': 'v_unprocessedviolation',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': '驾驶员/车主信息管理', 'verbose_name_plural': '驾驶员/车主信息管理'},
        ),
        migrations.AlterModelOptions(
            name='vehicle',
            options={'verbose_name': '机动车信息管理', 'verbose_name_plural': '机动车信息管理'},
        ),
        migrations.AlterModelOptions(
            name='violation',
            options={'verbose_name': '违章信息管理', 'verbose_name_plural': '违章信息管理'},
        ),
        migrations.AlterField(
            model_name='driverlicense',
            name='user_profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='TrafficMan.userprofile', verbose_name='姓名(身份证号)'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户名'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='engine_id',
            field=models.CharField(max_length=25, primary_key=True, serialize=False, verbose_name='机动车VIN编号'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TrafficMan.userprofile', verbose_name='车主'),
        ),
        migrations.AlterField(
            model_name='vehiclelicense',
            name='usage',
            field=models.CharField(choices=[('A', 'A-非营运'), ('B', 'B-公路客运'), ('C', 'C-公交客运'), ('D', 'D-出租客运'), ('E', 'E-旅游客运'), ('F', 'F-货运'), ('G', 'G-租赁'), ('H', 'H-警用'), ('I', 'I-消防'), ('J', 'J-救护'), ('K', 'K-工程抢险'), ('L', 'L-营转非'), ('M', 'M-出租转非'), ('N', 'N-教练'), ('R', 'R-化工'), ('Z', 'Z-其它')], max_length=20, verbose_name='使用性质'),
        ),
        migrations.AlterField(
            model_name='vehiclelicense',
            name='vehicle',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='TrafficMan.vehicle', verbose_name='车牌号'),
        ),
        migrations.AlterField(
            model_name='violation',
            name='deadline',
            field=models.DateField(verbose_name='罚款缴纳截至日期'),
        ),
        migrations.AlterField(
            model_name='violation',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TrafficMan.userprofile', verbose_name='驾驶员'),
        ),
        migrations.AlterField(
            model_name='violation',
            name='is_processed',
            field=models.BooleanField(verbose_name='是否缴纳'),
        ),
        migrations.AlterField(
            model_name='violation',
            name='plate_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TrafficMan.vehicle', to_field='plate_number', verbose_name='车牌号/车主/机动车VIN号'),
        ),
        migrations.AlterField(
            model_name='violation',
            name='type',
            field=models.CharField(max_length=100, verbose_name='违章类型'),
        ),
        migrations.CreateModel(
            name='ViolationProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_time', models.DateTimeField(verbose_name='处理时间')),
                ('violation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='TrafficMan.violation', verbose_name='违章编号')),
            ],
            options={
                'verbose_name': '违章处理查询',
                'verbose_name_plural': '违章处理查询',
            },
        ),
    ]
