from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Needy, Mosque, CustomUser, RessourceType, Ressource,Distribution
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    """Define admin pages for user"""
    ordering = ['id']
    list_display = ['first_name', 'last_name', 'email']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name','mosque','is_mosque_admin')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'mosque',
                'is_mosque_admin',
                'password',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Needy)
admin.site.register(Mosque)
admin.site.register(RessourceType)
admin.site.register(Ressource)
admin.site.register(Distribution)