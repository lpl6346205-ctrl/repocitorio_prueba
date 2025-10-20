from django.contrib import admin
from .models import SystemUser, Role

@admin.register(SystemUser)
class SystemUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'role', 'person')
    search_fields = ('username',)
    list_filter = ('role',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
