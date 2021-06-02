from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Contact, Employee, Task, ServiceRequest


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'name', 'phno', 'city')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'phno', 'address', 'city', 'date_joined')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active',)}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Contact)

admin.site.register(Employee)


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('task', 'request_placed_employee')
    ordering = ('task', 'request_placed_employee')
    search_fields = ('task', 'request_placed_employee')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('category', 'description', 'status', 'city', 'employer', 'employee')
    ordering = ('category', 'status')
    search_fields = ('category', 'status', 'city')
