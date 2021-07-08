from django.contrib import admin
from .models import User, Gender
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdminConfig(UserAdmin):
    ordering = ('email', 'reader_id',)
    list_display = ('email', 'first_name', 'last_name', 'gender',
                    'birth_date', 'reader_id')

    fieldsets = (
        ('Overview', {'fields': ('email', 'first_name', 'last_name', 'gender',
                                 'birth_date', 'reader_id', 'image_url', 'date_joined',
                                  'is_active')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'gender',
                       'birth_date', 'reader_id', 'image_url', 'date_joined',
                       'is_staff', 'is_active', 'is_superuser'),
        }),
    )

@admin.register(Gender)
class GenderAdminConfig(admin.ModelAdmin):
    list_display = ('title',)