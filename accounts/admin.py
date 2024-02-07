from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Role


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "id",
        "phonenumber",
        "username",
        "email",
        "firstname",
        "lastname",
        "is_staff",
        "is_profile_updated",
        "country",
        "city",
        "address_line1",
        "address_line2",
        "is_active",
        "date_joined",
    )
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("phonenumber", "firstname", "lastname")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role)
