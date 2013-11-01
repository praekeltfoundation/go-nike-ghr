from django.contrib import admin
from models import Province, District, Sector
from ghr.actions import export_select_fields_csv_action


class ProvinceAdmin(admin.ModelAdmin):
    actions = [export_select_fields_csv_action("Export selected objects as CSV file")]
    list_display = ["name"]


class DistrictAdmin(admin.ModelAdmin):
    actions = [export_select_fields_csv_action("Export selected objects as CSV file")]
    list_display = ["name", "district_province"]


class SectorAdmin(admin.ModelAdmin):
    actions = [export_select_fields_csv_action("Export selected objects as CSV file")]
    list_display = ["name", "sector_district", "belongs_to_province"]


    def belongs_to_province(self, obj):
        return "%s" % obj.sector_district.district_province.name

    belongs_to_province.short_description = "Province"


admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Sector, SectorAdmin)
