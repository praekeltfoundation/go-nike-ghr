import xlrd
import json
import os
import csv

"""
Output Format:
[
    {
        "pk": 1,
        "model": "hierarchy.province",
        "fields": {
            "name": "Northern Province"
        }
    },
    {
        "pk": 1,
        "model": "hierarchy.district",
        "fields": {
            "district_province": 1,
            "name": "Mungwi"
        }
    },
    {
        "pk": 1,
        "model": "hierarchy.sector",
        "fields": {
            "name": "Mesenge",
            "sector_district": 1
        }
    },
    {
        "pk": 2,
        "model": "hierarchy.sector",
        "fields": {
            "name": "Kasama",
            "sector_district": 1
        }
    }
]
"""

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
# The source file for the input can be found in:
# https://docs.google.com/a/westerncapelabs.com/spreadsheet/ccc?key=0AmwmKPwpRiVpdFFmSFZ1Ti1NNlY3RDBhXzlqalBQemc#gid=0
# and the file should be placed in the project root
input_file = os.path.join(PROJECT_ROOT, "province_district_sector.xlsx")
output_file = os.path.join(PROJECT_ROOT, "hierarchy", "fixtures", "hierarchy_upload.json")

# Workbook and worksheets
wb = xlrd.open_workbook(input_file)
ws = wb.sheet_by_name(u'Sheet1')

# Output json
output_json = []

# Primary Keys
province_pk = 0
district_pk = 0
sector_pk = 0

for rownum in range(ws.nrows):
    data = ws.row_values(rownum)
    if data[0] == "Province":  # Skipping the first entry of the list
        continue
    elif data[0]:
        province_pk = province_pk + 1
        output_json.append({"pk": province_pk,
                           "model": "hierarchy.province",
                           "fields": {"name": data[0]}}) # Dictionary to populate the json object



    if data[1] == "District":  # Skipping the first entry of the list
        continue
    elif data[1]:
        district_pk = district_pk + 1
        output_json.append({"pk": district_pk,
                            "model": "hierarchy.district",
                            "fields": {"name": data[1], "district_province": province_pk}}) # Dictionary to populate the json object


    if data[2] == "Sector":  # Skipping the first entry of the list
        continue
    elif data[2]:
        sector_pk = sector_pk + 1
        output_json.append({"pk": sector_pk,
                            "model": "hierarchy.sector",
                            "fields": {"name": data[2], "sector_district": district_pk}}) # Dictionary to populate the json object

with open(output_file, 'w') as outfile:
        json.dump(output_json, outfile, indent=4, separators=(',', ': '))
