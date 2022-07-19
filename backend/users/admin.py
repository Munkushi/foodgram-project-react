from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser



@register(CustomUser)
class UserAdmin_(UserAdmin):
    """Зарегистрировал модель юзер в админке."""
    list_display = (
        "id",
        "first_name", 
        "last_name", 
        "username", 
        "email",
        )

    search_fields = ("last_name", "email",)
    list_filter = ("email",)
