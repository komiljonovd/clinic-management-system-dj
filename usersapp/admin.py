from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# Register your models here.

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ['email']
    
    list_display = ['id', 'email','role','first_name','last_name','phone','date_joined', 'is_staff', 'is_active']
    list_display_links = ['id', 'email','role']
    search_fields = ['id', 'first_name', 'last_name', 'email', 'phone']
    list_filter = ['role', 'is_staff', 'is_active']
    list_per_page = 50
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone', 'role')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password','first_name','last_name','phone','role'),
        }),
    )
    
    readonly_fields = ['date_joined', 'last_login']

