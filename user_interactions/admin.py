from django.contrib import admin
from models import UserInteraction
from actions import export_as_csv_action


class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ["msisdn", "transport", "created_at"]

admin.site.register(UserInteraction, UserInteractionAdmin)
admin.site.add_action(export_as_csv_action(), "export csv")
