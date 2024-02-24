from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser, Role


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = "__all__"
        exclude = ("username",)


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = "__all__"
        exclude = ("username",)


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # Remove the 'username' field from the fieldsets
        fieldsets = list(fieldsets)
        for fieldset in fieldsets:
            if "username" in fieldset[1]["fields"]:
                fieldset[1]["fields"] = tuple(
                    field for field in fieldset[1]["fields"] if field != "username"
                )
        return fieldsets

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phonenumber", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "phonenumber",
        "email",
        "firstname",
        "lastname",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("phonenumber", "email", "firstname", "lastname")
    ordering = ("phonenumber",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role)
