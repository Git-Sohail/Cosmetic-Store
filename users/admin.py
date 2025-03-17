from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'full_name', 'profile_preview', 'phone_number', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')
    ordering = ('-date_joined',)
    list_per_page = 20
    actions = ['activate_users', 'deactivate_users']

    # Add our custom fields to the fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address'),
            'classes': ('wide', 'extrapretty')
        }),
        ('Profile Picture', {
            'fields': ('profile_picture', 'profile_preview'),
            'classes': ('wide', 'extrapretty')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('profile_preview',)
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'

    def profile_preview(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="width: 45px; height: 45px; object-fit: cover; '
                'border-radius: 50%; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.profile_picture.url
            )
        return format_html(
            '<div style="width: 45px; height: 45px; border-radius: 50%; '
            'background: linear-gradient(45deg, #ff3366, #ff9fb3); '
            'display: flex; align-items: center; justify-content: center;">'
            '<span style="color: white; font-size: 18px;">{}</span></div>',
            obj.first_name[0].upper() if obj.first_name else obj.username[0].upper()
        )
    profile_preview.short_description = 'Profile'

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users were successfully activated.')
    activate_users.short_description = "Activate selected users"

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users were successfully deactivated.')
    deactivate_users.short_description = "Deactivate selected users"

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
