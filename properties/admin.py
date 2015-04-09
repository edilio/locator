from django.contrib import admin
from models import *


class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'property_id', 'property_name', 'tracs_status',
                    'assisted_units', 'program_type')
    #list_display_links = ('phacode','haname')
    search_fields = ('contract_number', 'property_id', 'property_name')
    list_per_page = 25


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'county', 'state', 'zip_code', 'zip4_code')
    list_per_page = 25


class CountyAdmin(admin.ModelAdmin):
    list_display = ('code','name',)
    list_per_page = 25


class ManagementAgentAdmin(admin.ModelAdmin):
    list_display = ('company_type', '__unicode__',  # 'individual_full_name','organization_name',
                    'address_line1', 'address_line2', 'city', 'main_phone_number', #  'main_fax_number',
                    'email', 'properties', 'total_units')
    list_per_page = 13
    list_filter = ('company_type','city__state')
    search_fields = ('individual_full_name', 'organization_name')


class OwnerAdmin(admin.ModelAdmin):
    list_display = ('company_type', 'individual_title_text', 'individual_full_name', 'organization_name',
                    'address_line1', 'address_line2', 'city', 'main_phone_number', 'main_fax_number', 'email')
    list_per_page = 13
    list_filter = ('company_type','city__state')
    search_fields = ('individual_full_name','organization_name')


class PropertiesAdmin(admin.ModelAdmin):
    list_display = ('servicing_site_name', 'name', 'owner', 'management_agent', 'phone_number', 'city',
                    'property_total_unit_count', 'property_category_name')
    list_per_page = 13
    list_filter = ('city__state',)
    search_fields = ('name','owner__individual_full_name', 'owner__organization_name',
                     'management_agent__individual_full_name', 'management_agent__organization_name', 'phone_number')


def register(model, admin_class):
    admin.site.register(model, admin_class)

register(Contract, ContractAdmin)
register(County, CountyAdmin)
register(City, CityAdmin)
register(ManagementAgent,ManagementAgentAdmin)
register(Owner,OwnerAdmin)
register(Property,PropertiesAdmin)