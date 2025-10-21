from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Needy, Mosque, CustomUser, RessourceType, Ressource,Distribution,Notification, Document
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


class DistributionAdmin(admin.ModelAdmin):
    list_display = ['id', 'responsible', 'start_time', 'finish_time']
    list_filter = ['start_time', 'finish_time', 'responsible__mosque']
    search_fields = ['responsible__first_name', 'responsible__last_name', 'responsible__email']
    ordering = ['-start_time']




admin.site.register(CustomUser, UserAdmin)
admin.site.register(Needy)
admin.site.register(Mosque)
admin.site.register(RessourceType)
admin.site.register(Ressource)
admin.site.register(Distribution, DistributionAdmin)
admin.site.register(Notification)
admin.site.register(Document)