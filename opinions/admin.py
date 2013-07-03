from django.contrib import admin
from opinions.models import Opinion


class OpinionAdmin(admin.ModelAdmin):
    pass

# Registering the Article with the admin
admin.site.register(Opinion, OpinionAdmin)
