from django.contrib import admin
from models import (Category, SubCategory)
from django import forms
from django.forms.models import BaseInlineFormSet


class SubCategoryFormset(BaseInlineFormSet):
    def clean(self):
        super(SubCategoryFormset, self).clean()

        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue

            sub_cat_index = 0
            if ("name" not in form.cleaned_data and sub_cat_index >= 1):
                raise forms.ValidationError("You need to name the Sub Category")

            if ("name" in form.cleaned_data):
                if not (form.cleaned_data["content_1"] or
                        form.cleaned_data["content_2"] or
                        form.cleaned_data["content_3"]):
                    raise forms.ValidationError("You need to enter at least one "
                                                "screen of content to display")

            sub_cat_index = sub_cat_index + 1


class SubCategoryInline(admin.StackedInline):
    model = SubCategory
    extra = 0  # Number of initial answers fields
    formset = SubCategoryFormset


class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]

admin.site.register(Category, CategoryAdmin)
