from django.core.management import setup_environ
from django.core.management import execute_manager
#from django.db.models import Q

import imp
try:
    imp.find_module('settings') # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)

import settings
setup_environ(settings)
from properties.models import *

def get_city(name,state,zip_code,zip4_code):
    cities = City.objects.filter(
        name = name.strip(),
        state= state,
        zip_code = zip_code,
        zip4_code = zip4_code
    )
    if cities:
        return cities[0]
    else:
        county, created = County.objects.get_or_create(code='', name='')
        city = City(name=name.strip(), state=state, county=county,zip_code=zip_code,zip4_code=zip4_code)
        city.save()

        return city

counties = County.objects.all()
print len(counties)

contracts = Properties_Contracts.objects.all()[128:]
print len(contracts)


for contract in contracts:
    print contract.city_name_text
    temp = [county for county in counties if county.code == contract.county_code and county.name == contract.county_name_text.strip()]

    if temp:
        county = temp[0]
    else:
        county, created = County.objects.get_or_create(
            code = contract.county_code,
            name = contract.county_name_text.strip()
        )

    property_city, created = City.objects.get_or_create(
            name = contract.city_name_text.strip(),
            county = county,
            state = contract.state_code,
            zip_code = contract.zip_code,
            zip4_code = contract.zip4_code
        )


    owner_city = get_city(
        contract.owner_city_name,
        contract.owner_state_code,
        contract.owner_zip_code,
        contract.owner_zip4_code
    )

    temp = Owner.objects.filter(pk=contract.owner_participant_id)
    if temp:
        owner = temp[0]
    else:
        owner, created = Owner.objects.get_or_create(
            participant_id = contract.owner_participant_id,
            company_type = contract.owner_company_type.strip(),
            individual_first_name = contract.owner_individual_first_name.strip(),
            individual_middle_name = contract.owner_individual_middle_name.strip(),
            individual_last_name = contract.owner_individual_last_name.strip(),
            individual_full_name = contract.owner_individual_full_name.strip(),
            individual_title_text = contract.owner_individual_title_text.strip(),
            organization_name = contract.owner_organization_name.strip(),
            address_line1 = contract.owner_address_line1.strip(),
            address_line2 = contract.owner_address_line2.strip(),
            city = owner_city,
            main_phone_number = contract.owner_main_phone_number_text.strip(),
            main_fax_number = contract.owner_main_fax_number_text.strip(),
            email = contract.owner_email_text.strip(),
        )

    agent_city = get_city(
        name = contract.mgmt_agent_city_name,
        state= contract.mgmt_agent_state_code,
        zip_code = contract.mgmt_agent_zip_code,
        zip4_code = contract.mgmt_agent_zip4_code
    )

    temp = ManagementAgent.objects.filter(pk=contract.mgmt_agent_participant_id)
    if temp:
        agent = temp[0]
    else:
        agent, created = ManagementAgent.objects.get_or_create(
            participant_id = contract.mgmt_agent_participant_id,
            company_type = contract.mgmt_agent_company_type.strip(),
            individual_first_name = contract.mgmt_agent_indv_first_name.strip(),
            individual_last_name = contract.mgmt_agent_indv_last_name.strip(),
            individual_middle_name = contract.mgmt_agent_indv_middle_name.strip(),
            individual_full_name = contract.mgmt_agent_full_name.strip(),
            individual_title_text = contract.mgmt_agent_indv_title_text.strip(),
            organization_name = contract.mgmt_agent_org_name.strip(),
            address_line1 = contract.mgmt_agent_address_line1.strip(),
            address_line2 = contract.mgmt_agent_address_line2.strip(),
            city = agent_city,
            main_phone_number = contract.mgmt_agent_main_phone_number.strip(),
            main_fax_number = contract.mgmt_agent_main_fax_number.strip(),
            email = contract.mgmt_agent_email_text.strip(),
        )

    if contract.property_phone_number:
        property_phone = contract.property_phone_number.strip()
    else:
        property_phone = ""

    if contract.associated_financing_number:
        associated_financing_number = contract.associated_financing_number
    else:
        associated_financing_number = ""

    property = Property(
        property_id = contract.property_id,
        hub_name = contract.hub_name_text.strip(),
        servicing_site_name = contract.servicing_site_name_text.strip(),
        name = contract.property_name_text.strip(),
        phone_number = property_phone,
        address_line1_text = contract.address_line1_text.strip(),
        address_line2_text = contract.address_line2_text.strip(),
        city = property_city,
        msa_code = contract.msa_code,
        msa_name = contract.msa_name_text.strip(),
        congressional_district_code = contract.congressional_district_code.strip(),
        placed_base_city_name_text = contract.placed_base_city_name_text.strip(),
        property_total_unit_count = contract.property_total_unit_count,
        property_category_name = contract.property_category_name.strip(),
        primary_financing_type = contract.primary_financing_type.strip(),
        associated_financing_number = associated_financing_number,
        is_insured_ind = contract.is_insured_ind,
        is_202_811_ind = contract.is_202_811_ind,
        is_hud_held_ind = contract.is_hud_held_ind,
        is_hud_owned_ind = contract.is_hud_owned_ind,
        is_hospital_ind = contract.is_hospital_ind,
        is_nursing_home_ind = contract.is_nursing_home_ind,
        is_board_and_care_ind = contract.is_board_and_care_ind,
        is_assisted_living_ind = contract.is_assisted_living_ind,
        is_refinanced_ind = contract.is_refinanced_ind,
        is_221d3_ind = contract.is_221d3_ind,
        is_221d4_ind = contract.is_221d4_ind,
        is_236_ind = contract.is_236_ind,
        is_non_insured_ind = contract.is_non_insured_ind,
        is_bmir_ind = contract.is_bmir_ind,
        is_risk_sharing_ind = contract.is_risk_sharing_ind,
        is_mip_ind = contract.is_mip_ind,
        is_co_insured_ind = contract.is_co_insured_ind,
        ownership_effective_date = contract.ownership_effective_date,

        owner = owner,
        management_agent = agent
    )
    property.save()

print "Import completed for %d properties" %len(contracts)



##has = PHA.objects.filter(state ='CA')
##has.delete()