from django.contrib import admin
from models import (Category, SubCategory)
from django import forms
from django.forms.models import BaseInlineFormSet


class SubCategoryFormset(BaseInlineFormSet):
    pass


class SubCategoryInline(admin.StackedInline):
    model = SubCategory
    extra = 0  # Number of initial answers fields
    formset = SubCategoryFormset


class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]


class SubCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
# admin.site.register(SubCategory, SubCategoryAdmin)