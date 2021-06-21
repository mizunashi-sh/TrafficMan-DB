from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Gender(models.TextChoices):
    MALE = 'M', _('男')
    FEMALE = 'F', _('女')


class MotorType(models.TextChoices):
    A1 = 'A1', _('A1-大型客车')
    A2 = 'A2', _('A2-牵引车')
    A3 = 'A3', _('A3-城市公交车')
    B1 = 'B1', _('B1-中型客车')
    B2 = 'B2', _('B2-大型货车')
    C1 = 'C1', _('C1-小型汽车')
    C2 = 'C2', _('C2-小型自动挡汽车')
    C3 = 'C3', _('C3-低速载货汽车')
    C4 = 'C4', _('C4-三轮汽车')
    C5 = 'C5', _('C5-残疾人专用小型自动挡载客汽车')
    D = 'D', _('D-普通三轮摩托车')
    E = 'E', _('E-普通二轮摩托车')
    F = 'F', _('F-轻便摩托车')
    M = 'M', _('M-轮式自行机械车')
    N = 'N', _('N-无轨电车')
    P = 'P', _('P-有轨电车')


class DriverStatus(models.TextChoices):
    A = 'A', _('A-正常')
    B = 'B', _('B-超分')
    C = 'C', _('C-转出')
    D = 'D', _('D-暂扣')
    E = 'E', _('E-撤销')
    F = 'F', _('F-吊销')
    G = 'G', _('G-注销')
    H = 'H', _('H-违法未处理')
    J = 'J', _('J-停止使用')


class VehicleType(models.TextChoices):
    A = 'A', _('载货汽车')
    B = 'B', _('越野汽车')
    C = 'C', _('自卸汽车')
    D = 'D', _('牵引车')
    E = 'E', _('专用汽车')
    F = 'F', _('客车')
    G = 'G', _('轿车')
    H = 'H', _('半挂车')
    K = 'K', _('其它')


class VehicleStatus(models.TextChoices):
    A = 'A', _('A-正常')
    B = 'B', _('B-转出')
    C = 'C', _('C-被盗抢')
    D = 'D', _('D-停驶')
    E = 'E', _('E-注销')
    G = 'G', _('F-违法未处理')
    H = 'H', _('H-海关监管')
    Z = 'I', _('I-事故未处理')
    J = 'J', _('J-嫌疑车')
    K = 'K', _('K-查封')
    L = 'L', _('L-暂扣')
    M = 'M', _('M-强制注销')
    N = 'N', _('N-事故逃逸')
    P = 'O', _('O-锁定')
    F = 'F', _('F-退车')


class UsageType(models.TextChoices):
    A = 'A', _('A-非营运')
    B = 'B', _('B-公路客运')
    C = 'C', _('C-公交客运')
    D = 'D', _('D-出租客运')
    E = 'E', _('E-旅游客运')
    F = 'F', _('F-货运')
    G = 'G', _('G-租赁')
    H = 'H', _('H-警用')
    Y = 'I', _('I-消防')
    J = 'J', _('J-救护')
    K = 'K', _('K-工程抢险')
    L = 'L', _('L-营转非')
    M = 'M', _('M-出租转非')
    N = 'N', _('N-教练')
    R = 'R', _('R-化工')
    Z = 'Z', _('Z-其它')


class UserProfile(models.Model):
    """用户信息"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户名')
    identity = models.CharField('身份证号', max_length=25, primary_key=True)
    name = models.CharField('姓名', max_length=80)
    gender = models.CharField(
        '性别',
        max_length=5,
        choices=Gender.choices
    )
    ethnicity = models.CharField('民族', max_length=20)
    nationality = models.CharField('国籍', max_length=10)
    address = models.CharField('住址', max_length=200)
    telephone = models.CharField('固定电话', max_length=15)
    mobile = models.CharField('手机号码', max_length=25)
    birth = models.DateField('出生日期')

    def __str__(self):
        return self.name + '(' + self.identity + ')'

    class Meta:
        verbose_name_plural = "驾驶员/车主信息管理"
        verbose_name = "驾驶员/车主信息管理"


class DriverLicense(models.Model):
    """驾驶证信息"""

    user_profile = models.OneToOneField(UserProfile, primary_key=True, on_delete=models.CASCADE,
                                        verbose_name='姓名(身份证号)')
    issue_date = models.DateField('驾驶证初次领证日期')
    motor_type = models.CharField('驾驶证准驾车型', max_length=3, choices=MotorType.choices)
    begin_date = models.DateField('驾驶证有效起始日期')
    valid_duration = models.PositiveIntegerField('驾驶证有效年限（年）')
    points = models.IntegerField('驾驶证分数', default=12)
    status = models.CharField('驾驶证状态', max_length=5, choices=DriverStatus.choices, default=DriverStatus.A)

    def __str__(self):
        return str(self.user_profile)

    class Meta:
        verbose_name_plural = "驾驶证信息"
        verbose_name = "驾驶证信息"


class Vehicle(models.Model):
    """机动车"""

    engine_id = models.CharField('机动车VIN编号', max_length=25, primary_key=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='车主')
    brand = models.CharField('品牌', max_length=25)
    manufacture_model = models.CharField('型号', max_length=35)
    color = models.CharField('颜色', max_length=20)
    vehicle_type = models.CharField('车型', max_length=2, choices=VehicleType.choices)
    displacement = models.DecimalField('排量', max_digits=5, decimal_places=2)
    manufacture_date = models.DateField('出厂日期')
    life_duration = models.PositiveIntegerField('使用年限（年）')
    plate_number = models.CharField('车牌号码', max_length=20, unique=True, null=True)
    status = models.CharField('机动车状态', max_length=8, choices=VehicleStatus.choices, default=VehicleStatus.A)

    def __str__(self):
        return str(self.plate_number) + '/' + str(self.owner) + '/' + self.engine_id

    class Meta:
        verbose_name_plural = "机动车信息管理"
        verbose_name = "机动车信息管理"


class VehicleLicense(models.Model):
    """行驶证信息"""

    vehicle = models.OneToOneField(Vehicle, primary_key=True, on_delete=models.CASCADE, verbose_name='车牌号')
    usage = models.CharField('使用性质', max_length=20, choices=UsageType.choices)
    registration_date = models.DateField('注册日期')
    issue_date = models.DateField('发证日期')

    def __str__(self):
        return str(self.vehicle)

    class Meta:
        verbose_name_plural = "行驶证信息"
        verbose_name = "行驶证信息"


class Violation(models.Model):
    """违章"""
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name='车牌号/车主/机动车VIN号')
    driver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='驾驶员')
    date = models.DateTimeField('违章时间')
    type = models.CharField('违章类型', max_length=100)
    area = models.CharField('区域', max_length=50)
    location = models.CharField('位置', max_length=50)
    point_minus = models.PositiveIntegerField('扣分')
    fine = models.DecimalField('罚款', max_digits=5, decimal_places=2)
    deadline = models.DateField('罚款缴纳截至日期')
    is_processed = models.BooleanField('是否缴纳')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name_plural = "违章信息管理"
        verbose_name = "违章信息管理"


class ViolationProcess(models.Model):
    violation = models.OneToOneField(Violation, on_delete=models.CASCADE, verbose_name='违章编号',primary_key=True)
    process_time = models.DateTimeField('处理时间')

    class Meta:
        verbose_name_plural = '违章处理记录管理'
        verbose_name = '违章处理记录管理'


class Education(models.Model):
    driver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='驾驶员')
    create_time = models.DateTimeField('登记时间')
    is_finished = models.BooleanField('是否完成')

    class Meta:
        verbose_name_plural = '道路安全学习信息管理'
        verbose_name = '道路安全学习信息管理'


class EducationRecord(models.Model):
    education = models.OneToOneField(Education, on_delete=models.CASCADE, verbose_name='学习ID', primary_key=True)
    finish_time = models.DateTimeField('学习完成时间')

    class Meta:
        verbose_name_plural = '道路安全学习记录管理'
        verbose_name = '道路安全学习记录管理'


class OwnerVehicleView(models.Model):
    """机动车-车主联合查询视图"""
    identity = models.CharField('车主身份证号', max_length=25)
    name = models.CharField('车主姓名', max_length=80)
    gender = models.CharField(
        '性别',
        max_length=5,
        choices=Gender.choices
    )
    ethnicity = models.CharField('民族', max_length=20)
    nationality = models.CharField('国籍', max_length=10)
    address = models.CharField('住址', max_length=200)
    telephone = models.CharField('固定电话', max_length=15)
    mobile = models.CharField('手机号码', max_length=25)
    birth = models.DateField('出生日期')
    engine_id = models.CharField('机动车VIN编号', max_length=25, primary_key=True)
    brand = models.CharField('品牌', max_length=25)
    manufacture_model = models.CharField('型号', max_length=35)
    color = models.CharField('颜色', max_length=20)
    vehicle_type = models.CharField('车型', max_length=2, choices=VehicleType.choices)
    displacement = models.DecimalField('排量', max_digits=5, decimal_places=2)
    manufacture_date = models.DateField('出厂日期')
    life_duration = models.PositiveIntegerField('使用年限（年）')
    plate_number = models.CharField('车牌号码', max_length=20)
    status = models.CharField('机动车状态', max_length=8, choices=VehicleStatus.choices, default=VehicleStatus.A)

    class Meta:
        managed = False
        db_table = 'v_vehicleowner'
        verbose_name_plural = "机动车-车主信息联合查询"
        verbose_name = "机动车-车主信息联合查询"


class ExceededViolationView(models.Model):
    """过期违章查询视图"""
    date = models.DateTimeField('违章时间')
    location = models.CharField('区域', max_length=50)
    type = models.CharField('违章类型', max_length=100)
    deadline = models.DateField('罚款缴纳截至日期')
    fine = models.DecimalField('罚款', max_digits=5, decimal_places=2)
    plate_number = models.CharField('车牌号码', max_length=20)
    driver_id = models.CharField('驾驶员身份证号', max_length=25)
    driver_name = models.CharField('驾驶员姓名', max_length=80)
    owner_id = models.CharField('车主身份证号', max_length=25)
    owner_name = models.CharField('车主姓名', max_length=80)
    is_processed = models.BooleanField('是否缴纳')

    class Meta:
        managed = False
        db_table = 'v_exceededviolation'
        verbose_name_plural = "逾期违章查询"
        verbose_name = "逾期违章查询"


class UnprocessedViolationView(models.Model):
    """未处理违章查询视图"""
    date = models.DateTimeField('违章时间')
    area = models.CharField('区域', max_length=50)
    type = models.CharField('违章类型', max_length=100)
    deadline = models.DateField('罚款缴纳截至日期')
    fine = models.DecimalField('罚款', max_digits=5, decimal_places=2)
    plate_number = models.CharField('车牌号码', max_length=20)
    driver_id = models.CharField('驾驶员身份证号', max_length=25)
    driver_name = models.CharField('驾驶员姓名', max_length=80)
    owner_id = models.CharField('车主身份证号', max_length=25)
    owner_name = models.CharField('车主姓名', max_length=80)
    is_processed = models.BooleanField('是否缴纳')

    class Meta:
        managed = False
        db_table = 'v_unprocessedviolation'
        verbose_name_plural = "未处理违章查询"
        verbose_name = "未处理违章查询"


class ViolationProcessRecordView(models.Model):
    """违章处理记录查询视图"""
    date = models.DateTimeField('违章时间')
    type = models.CharField('违章类型', max_length=100)
    area = models.CharField('区域', max_length=50)
    location = models.CharField('位置', max_length=50)
    point_minus = models.PositiveIntegerField('扣分')
    fine = models.DecimalField('罚款', max_digits=5, decimal_places=2)
    deadline = models.DateField('罚款缴纳截至日期')
    is_processed = models.BooleanField('是否缴纳')
    driver_id = models.CharField('驾驶员身份证号', max_length=25)
    plate_number = models.CharField('车牌号码', max_length=20)
    process_time = models.DateTimeField('处理时间')

    class Meta:
        managed = False
        db_table = 'v_violationprocessrecord'
        verbose_name_plural = "违章处理记录查询"
        verbose_name = "违章处理记录查询"
