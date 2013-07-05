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
        Modifying the data to provide the quiz and answers and responses.
        Structure is {{{}}}
        This function handles /api/weeklyquiz/
        """
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                del(data_dict['meta'])

            if data_dict["objects"] == []:
                data_dict['quiz'] = False
                del (data_dict['objects'])
            else:
                directory = {}  # Variable to hold directory structure
                category_obj = data_dict["objects"]
                for category_i in range(len(category_obj)):
                    category_name = category_obj[category_i].data["name"]
                    sub_category_obj = category_obj[category_i].data["category"]

                    sub_category_dict = {}
                    for sub_category_i in range(len(sub_category_obj)):
                        sub_category_content = {}
                        sub_category_obj_data = sub_category_obj[sub_category_i].data
                        for key, value in sub_category_obj_data.iteritems():
                            if key in ["content_1", "content_2", "content_3"]:
                                sub_category_content[key] = value
                        sub_category_dict[sub_category_obj_data["name"]] = sub_category_content

                    directory[category_name] = sub_category_dict
                data_dict['directory'] = directory
                del (data_dict['objects'])
        return data_dict


class SubCategoryResource(ModelResource):
    class Meta:
        queryset = SubCategory.objects.all()
