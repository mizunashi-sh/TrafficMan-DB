from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from .models import Vehicle
from .models import VehicleLicense
from .models import Violation
from .models import UserProfile
from .models import DriverLicense
from .models import Education
from .models import OwnerVehicleView
from .models import ExceededViolationView
from .models import UnprocessedViolationView
from .models import ViolationProcessRecordView

admin.site.site_header = '道路交通违章信息管理系统控制台'
admin.site.site_title = "道路交通违章信息管理系统控制台"


class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UserInline,)


class EducationInline(admin.TabularInline):
    model = Education
    can_delete = False
    readonly_fields = ('driver', 'create_time')

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


class VehicleLicenseInline(admin.StackedInline):
    model = VehicleLicense

    def has_add_permission(self, request, obj):
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        user = User.objects.get(id=request.user.id)
        groups = user.groups.all().values_list('name', flat=True)
        if 'superior_staff' in groups:
            return True
        return False


class ViolationInlineForVehicle(admin.TabularInline):
    model = Violation
    can_delete = False
    show_change_link = True
    fields = ('driver', 'date', 'location', 'point_minus', 'fine', 'deadline', 'is_processed')
    readonly_fields = ('driver', 'date', 'location', 'point_minus', 'fine', 'deadline', 'is_processed')
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'engine_id', 'plate_number', 'brand', 'manufacture_model', 'owner', 'vehicle_type', 'manufacture_date',
        'status')
    search_fields = ('plate_number', 'engine_id', 'brand', 'manufacture_model', 'owner__name', 'owner__identity')
    list_filter = ('vehicle_type', 'status')
    autocomplete_fields = ('owner',)
    inlines = (VehicleLicenseInline, ViolationInlineForVehicle)

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        user = User.objects.get(id=request.user.id)
        groups = user.groups.all().values_list('name', flat=True)
        if 'superior_staff' in groups:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


class DriverLicenseInline(admin.StackedInline):
    model = DriverLicense
    can_delete = False

    def has_add_permission(self, request, obj):
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        user = User.objects.get(id=request.user.id)
        groups = user.groups.all().values_list('name', flat=True)
        if 'superior_staff' in groups:
            return True
        return False


class VehicleInline(admin.TabularInline):
    model = Vehicle
    can_delete = False
    show_change_link = True
    fields = ('plate_number', 'engine_id', 'brand', 'manufacture_model')
    readonly_fields = ('plate_number', 'engine_id', 'brand', 'manufacture_model')
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ViolationInlineForUser(admin.TabularInline):
    model = Violation
    can_delete = False
    show_change_link = True
    fields = ('vehicle', 'date', 'location', 'point_minus', 'fine', 'deadline', 'is_processed')
    readonly_fields = ('vehicle', 'date', 'location', 'point_minus', 'fine', 'deadline', 'is_processed')
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ('name', 'identity')
    list_display = ('name', 'identity', 'gender', 'mobile')
    autocomplete_fields = ('user',)
    inlines = [DriverLicenseInline, EducationInline, VehicleInline, ViolationInlineForUser]

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        user = User.objects.get(id=request.user.id)
        groups = user.groups.all().values_list('name', flat=True)
        if 'superior_staff' in groups:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


class ViolationAdmin(admin.ModelAdmin):
    list_filter = ('is_processed',)
    list_display = ('id', 'vehicle', 'driver', 'date', 'type', 'deadline', 'is_processed')
    search_fields = (
        'id', 'type', 'area', 'location', 'vehicle__plate_number', 'driver__name', 'driver__identity',
        'vehicle__owner__name', 'vehicle__owner__identity')
    autocomplete_fields = ('vehicle', 'driver',)

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        user = User.objects.get(id=request.user.id)
        groups = user.groups.all().values_list('name', flat=True)
        if 'superior_staff' in groups:
            return True
        return False


class OwnerVehicleAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'name', 'identity', 'brand', 'manufacture_model', 'status')
    search_fields = (
        'identity', 'name', 'brand', 'manufacture_model', 'vehicle_type', 'plate_number')
    list_filter = ('status', 'vehicle_type')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ExceededViolationAdmin(admin.ModelAdmin):
    search_fields = (
        'id', 'type', 'location', 'plate_number', 'driver_name', 'driver_id', 'owner_name', 'owner_id')
    list_display = (
        'id', 'plate_number', 'date', 'type', 'fine', 'deadline', 'driver_name', 'driver_id', 'owner_name', 'owner_id')
    readonly_fields = (
        'id', 'date', 'location', 'type', 'deadline', 'fine', 'plate_number', 'driver_id', 'driver_name', 'owner_id',
        'owner_name')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class UnprocessedViolationAdmin(admin.ModelAdmin):
    search_fields = (
        'id', 'type', 'area', 'plate_number', 'driver_name', 'driver_id', 'owner_name', 'owner_id')
    list_display = (
        'id', 'plate_number', 'date', 'type', 'fine', 'deadline', 'driver_name', 'driver_id', 'owner_name', 'owner_id')
    readonly_fields = (
        'id', 'date', 'area', 'type', 'deadline', 'fine', 'plate_number', 'driver_id', 'driver_name', 'owner_id',
        'owner_name')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ViolationProcessRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'type', 'plate_number', 'driver_id', 'deadline', 'process_time')
    search_fields = ('id', 'type', 'area', 'location', 'plate_number', 'driver_id')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(OwnerVehicleView, OwnerVehicleAdmin)
admin.site.register(ExceededViolationView, ExceededViolationAdmin)
admin.site.register(UnprocessedViolationView, UnprocessedViolationAdmin)
admin.site.register(ViolationProcessRecordView, ViolationProcessRecordAdmin)

admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Violation, ViolationAdmin)
