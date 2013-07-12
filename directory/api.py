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
    path = 'directory.api.SubCategoryResource'
    category = fields.ToManyField(path, 'category', full=True)

    class Meta:
        # setting the resoucrce attributes
        resource_name = "category"
        allowed_methods = ['get']
        excludes = ['completed', 'active']
        include_resource_uri = False
        queryset = Category.objects.all()

    def alter_list_data_to_serialize(self, request, data_dict):
        """
        Modifying the data to provide the Categories and Sub Categories.
        Structure is {dir: {cat: {sub_cat{c: "a", c2: "b", "c3: "c"}}}}
        This function handles /api/category/
        """
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])

            if data_dict["objects"] != []:
                directory = {}  # Variable to hold directory structure
                category_obj = data_dict["objects"]

                for category_bundle in category_obj:
                    category_name = category_bundle.data["name"]
                    sub_category_obj = category_bundle.data["category"]

                    sub_category_dict = {}  # Dict for holding sub categories
                    for sub_category_bundle in sub_category_obj:
                        sub_cat_content = {}  # Dict for holding sub categories content
                        sub_cat_obj_data = sub_category_bundle.data
                        for key, value in sub_cat_obj_data.iteritems():
                            if key in ["content_1", "content_2", "content_3"]:
                                sub_cat_content[key] = value
                        sub_category_dict[sub_cat_obj_data["name"]] = sub_cat_content

                    directory[category_name] = sub_category_dict
                data_dict['directory'] = directory

            del data_dict['objects']
        return data_dict


class SubCategoryResource(ModelResource):
    class Meta:
        queryset = SubCategory.objects.all()
