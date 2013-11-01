from tastypie.resources import ModelResource
from tastypie import fields
from models import Province, District, Sector
from tastypie.resources import ALL_WITH_RELATIONS, ALL


class DistrictResource(ModelResource):
    """
    This class:
        - Adds resource_name for the API
        - Returns the required data for the API via Foreign key association,
        based on the url
    """
    class Meta:
        resource_name = "district"
        allowed_methods = ['get']
        include_resource_uri = True
        queryset = District.objects.all()


class SectorResource(ModelResource):
    """
    This class:
        - Adds resource_name for the API
        - Returns the required data for the API via Foreign key association,
        based on the url
    """
    sector_district = fields.ForeignKey(DistrictResource,
                                        'sector_district',
                                        full=True)
    class Meta:
        resource_name = "sector"
        allowed_methods = ['get']
        include_resource_uri = True
        queryset = Sector.objects.all()
        max_limit = None
