import datetime
from dateutil.relativedelta import relativedelta

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from .models import UserProfile
from .models import DriverLicense
from .models import Vehicle
from .models import VehicleLicense
from .models import Violation


# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'auth.html')
    username = request.POST.get("username")
    password = request.POST.get("password")
    is_clicked = request.POST.get("login_button")
    if not is_clicked:
        user_obj = auth.authenticate(username=username, password=password)
        if user_obj:
            auth.login(request, user_obj)
            path = request.GET.get("next") or "/dashboard/"
            return redirect(path)
        else:
            error_msg = "请输入正确的用户名和密码"
            return render(request, 'auth.html', {'error_msg': error_msg})


@login_required(login_url='/auth/')
def dashboard(request):
    context = {}
    no_info_msg = '暂无个人信息'
    no_driverlicense_msg = "暂无驾驶证信息"
    username = request.user.username
    user_info = UserProfile.objects.filter(user__id=request.user.id)
    driver_license = DriverLicense.objects.filter(user_profile__user__id=request.user.id)

    context['username'] = username
    context['is_warning'] = False
    if len(user_info) == 0:
        context['no_info_msg'] = no_info_msg
        context['no_driverlicense_msg'] = no_driverlicense_msg
        return render(request, 'dashboard.html', context)

    if len(driver_license) == 0:
        context['user_info'] = user_info[0]
        context['no_driverlicense_msg'] = no_driverlicense_msg
        return render(request, 'dashboard.html', context)
    else:
        context['user_info'] = user_info[0]
        context['driver_license'] = driver_license[0]
        license_expire_date = driver_license[0].begin_date + relativedelta(years=driver_license[0].valid_duration)
        today = datetime.date.today()
        interval = license_expire_date - today

        if interval.days >= 0 and interval.days <= 30:
            context['is_warning'] = True
            context['warning_msg'] = '您的驾驶证还有' + str(interval.days) + '天到期，请及时至相关主管部门办理换发手续。'
        elif interval.days < 0:
            context['is_warning'] = True
            context['warning_msg'] = '您的驾驶证已经到期，请及时至相关主管部门办理相关手续，未办理相关手续超过一年的驾驶证可能会被吊销。'
        return render(request, 'dashboard.html', context)


@login_required(login_url='/auth/')
def my_vehicle(request):
    username = request.user.username
    no_vehicle_msg = '找不到机动车信息'
    search_text = request.GET.get("search")
    if search_text:
        vehicles = Vehicle.objects.filter(
            owner__user__id=request.user.id,
        ).filter(
            Q(plate_number__contains=search_text) | Q(brand__contains=search_text)
        )
    else:
        vehicles = Vehicle.objects.filter(owner__user__id=request.user.id)

    if len(vehicles) == 0:
        return render(request, 'my_vehicle.html', {'username': username, 'no_vehicle_msg': no_vehicle_msg})
    return render(request, 'my_vehicle.html', {'username': username, 'vehicle_list': vehicles})


@login_required(login_url='/auth/')
def vehicle_info(request, vin):
    username = request.user.username
    vehicle = Vehicle.objects.filter(engine_id=vin)
    if len(vehicle) == 0:
        return render(request, '404.html', status=404)
    vehicle_owner_id = vehicle[0].owner.user.id
    if request.user.id != vehicle_owner_id:
        return render(request, '403.html', status=403)

    license_info = VehicleLicense.objects.filter(vehicle__engine_id=vin)
    no_license_msg = '此车辆暂无行驶证信息'
    if len(license_info) == 0:
        return render(request, 'vehicle_detail.html',
                      {'username': username, 'vehicle_info': vehicle[0], 'no_license_msg': no_license_msg})
    return render(request, 'vehicle_detail.html',
                  {'username': username, 'vehicle_info': vehicle[0], 'license_info': license_info[0]})


@login_required(login_url='/auth/')
def violation(request):
    return redirect('/violations/user')


@login_required(login_url='/auth/')
def user_violation(request):
    username = request.user.username
    no_violation_msg = '暂无违章信息'
    violations = Violation.objects.filter(driver__user__id=request.user.id).order_by('-id')
    if len(violations) == 0:
        return render(request,
                      'violations.html',
                      {'username': username, 'no_violation_msg': no_violation_msg, 'type': 'user'})

    paginator = Paginator(violations, 10)
    page = request.GET.get('page')
    try:
        violation_list = paginator.page(page)
    except PageNotAnInteger:
        violation_list = paginator.page(1)
    except EmptyPage:
        violation_list = paginator.page(paginator.num_pages)

    return render(request,
                  'violations.html',
                  {'username': username, 'violation_list': violation_list, 'type': 'user'})


@login_required(login_url='/auth/')
def vehicle_violation(request):
    username = request.user.username
    no_violation_msg = '暂无违章信息'
    violations = Violation.objects.filter(vehicle__owner__user__id=request.user.id).order_by('-id')
    if len(violations) == 0:
        return render(request,
                      'violations.html',
                      {'username': username, 'no_violation_msg': no_violation_msg, 'type': 'vehicle'})

    paginator = Paginator(violations, 10)
    page = request.GET.get('page')
    try:
        violation_list = paginator.page(page)
    except PageNotAnInteger:
        violation_list = paginator.page(1)
    except EmptyPage:
        violation_list = paginator.page(paginator.num_pages)

    return render(request,
                  'violations.html',
                  {'username': username, 'violation_list': violation_list, 'type': 'vehicle'})


@login_required(login_url='/auth/')
def violation_info(request, violation_id):
    username = request.user.username
    violation = Violation.objects.filter(id=violation_id)
    if len(violation) == 0:
        return render(request, '404.html', status=404)
    driver_info = UserProfile.objects.filter(user__id=violation[0].driver.user.id)
    owner_info = UserProfile.objects.filter(user__id=violation[0].vehicle.owner.user.id)
    if driver_info[0].user.id != request.user.id and owner_info[0].user.id != request.user.id:
        return render(request, '403.html', status=403)

    return render(request,
                  'violation_detail.html',
                  {'username': username, 'violation': violation[0], 'driver': driver_info[0], 'owner': owner_info[0]})


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def permission_denied(request, exception):
    return render(request, '403.html', status=403)


def internal_error(request):
    return render(request, '500.html', status=500)


def logout(request):
    auth.logout(request)
    return redirect('/auth/')
