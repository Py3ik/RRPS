from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# Регистрация UserProfile как inline в админке User
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'

# Расширение стандартной админки User
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

# Перерегистрируем модель User с добавлением UserProfile
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)