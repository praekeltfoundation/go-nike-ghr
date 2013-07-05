from tastypie.resources import ModelResource
from tastypie import fields
from directory.models import (Category, SubCategory)


class CategoryResource(ModelResource):
    """
    This class:
        - Adds resource_name for the API
        - Returns the required data for the API via Foreign key association,
        based on the url
    """
    path = 'directory.api.WeeklyQuizQuestionResource'
    category = fields.ToManyField(path, 'category', full=True)

    class Meta:
        # setting the resoucrce attributes
        resource_name = "category"
        allowed_methods = ['get']
        excludes = ['completed', 'active']
        include_resource_uri = False
        queryset = Category.objects.all()