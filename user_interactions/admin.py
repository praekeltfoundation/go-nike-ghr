from django.contrib import admin
from models import UserInteraction


class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ["msisdn", "transport", "created_at"]

admin.site.register(UserInteraction, UserInteractionAdmin)
