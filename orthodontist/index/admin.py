from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ['user', 'image']
    verbose_name = 'Фото профиля'
    verbose_name_plural = 'Фото'
    can_delete = False


class MyUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    readonly_fields = ['email']
    fieldsets = (
        ('Личная информация', {'fields': ('username', 'password', 'first_name', 'last_name', 'email')}),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )


admin.site.register(User, MyUserAdmin)
