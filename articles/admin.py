from django.contrib import admin
from articles.models import Article

# Registering the Article with the admin
admin.site.register(Article)
