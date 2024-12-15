from django.contrib import admin
from .models import Vehiculo, User
from django.contrib.auth.admin import UserAdmin


class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'serial_carroceria', 'serial_motor', 'categoria', 'precio', 'fecha_creacion', 'fecha_modificacion')
    list_filter = ('marca', 'categoria', 'precio', 'fecha_creacion')
    search_fields = ('marca', 'modelo', 'serial_carroceria', 'serial_motor')

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active', 'role')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )


    
admin.site.register(User, CustomUserAdmin)
