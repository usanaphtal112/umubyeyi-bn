from django.contrib import admin
from .models import CustomUser, BlacklistedToken
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ("id", "phone_number", "first_name", "last_name", "role")
    search_fields = ("phone_number", "first_name", "last_name")
    ordering = ("phone_number",)
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("role",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "role",
                ),
            },
        ),
    )


class BlacklistedTokenAdmin(admin.ModelAdmin):
    list_display = ("token", "blacklisted_at")
    search_fields = ("token",)
    ordering = ("blacklisted_at",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(BlacklistedToken, BlacklistedTokenAdmin)
