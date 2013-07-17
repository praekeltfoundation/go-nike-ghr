from django.contrib import admin
from models import UserInteraction
from actions import export_as_csv_action


class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ["msisdn", "feature", "transport", "created_at"]
    actions = [export_as_csv_action("Export selected objects as CSV file",
                                    fields=["msisdn", "feature", "key", "value",
                                            "transport", "created_at"])]

admin.site.register(UserInteraction, UserInteractionAdmin)
