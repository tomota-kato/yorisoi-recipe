from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'プロフィール'
    fields = [
        'bio', 'avatar', 'birth_date', 
        'favorite_cuisine', 'dietary_restrictions',
        'email_notifications'
    ]


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# 既存のUserAdminを削除して新しいものを登録
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'full_name', 'favorite_cuisine', 
        'email_notifications', 'created_at'
    ]
    list_filter = ['email_notifications', 'created_at']
    search_fields = ['user__username', 'user__email', 'bio']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
