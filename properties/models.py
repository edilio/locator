from django.db import models
from localflavor.us.models import *
from django.utils.translation import gettext_lazy as _


class County(models.Model):
    code = models.CharField(max_length=3, blank=True)
    name = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name_plural = _("Counties")

    def __unicode__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=30)
    county = models.ForeignKey(County)
    state = USStateField()
    zip_code = models.CharField(max_length=5, blank=True)
    zip4_code = models.CharField(max_length=4, blank=True)

    class Meta:
        verbose_name_plural = _("Cities")

    def __unicode__(self):
        return self.name


class Contract(models.Model):
    contract_number = models.CharField(max_length=11, blank=True, primary_key=True)
    property_id = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    property_name = models.CharField(max_length=50, blank=True, db_column=u'property_name_text')
    tracs_status = models.CharField(max_length=20, blank=True, db_column=u'tracs_status_name')
    assisted_units = models.DecimalField(null=True, max_digits=5, decimal_places=0, blank=True,
                                         db_column=u'assisted_units_count')
    program_type = models.CharField(max_length=20, blank=True, db_column=u'program_type_name')
    br0_count = models.FloatField(null=True, db_column=u'0BR_count', blank=True)
    one_br_count = models.FloatField(null=True, db_column=u'1BR_count', blank=True)
    two_br_count = models.FloatField(null=True, db_column=u'2BR_count', blank=True)
    Three_br_count = models.FloatField(null=True, db_column=u'3BR_count', blank=True)
    four_br4_count = models.FloatField(null=True, db_column=u'4BR_count', blank=True)
    five_plus_br_count = models.FloatField(null=True, db_column=u'5plusBR_count', blank=True)

    class Meta:
        db_table = u'Contracts'

    def __unicode__(self):
        return self.contract_number


class Owner(models.Model):
    participant_id = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0, editable=False)
    company_type = models.CharField(max_length=20, blank=True)
    individual_first_name = models.CharField(max_length=18, blank=True)
    individual_middle_name = models.CharField(max_length=18, blank=True)
    individual_last_name = models.CharField(max_length=20, blank=True)
    individual_full_name = models.CharField(max_length=60, blank=True)
    individual_title_text = models.CharField(max_length=100, blank=True)
    organization_name = models.CharField(max_length=100, blank=True)
    address_line1 = models.CharField(max_length=45, blank=True)
    address_line2 = models.CharField(max_length=45, blank=True)
    city = models.ForeignKey(City, blank=True)
    main_phone_number = models.CharField(max_length=25, blank=True)
    main_fax_number = models.CharField(max_length=25, blank=True)
    email = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        if self.individual_full_name:
            return self.individual_full_name
        else:
            return self.organization_name


class ManagementAgent(models.Model):
    participant_id = models.DecimalField(primary_key=True,max_digits=10, decimal_places=0, editable=False)
    company_type = models.CharField(max_length=20, blank=True)
    individual_first_name = models.CharField(max_length=18, blank=True)
    individual_last_name = models.CharField(max_length=18, blank=True)
    individual_middle_name = models.CharField(max_length=18, blank=True)
    individual_full_name = models.CharField(max_length=56, blank=True)
    individual_title_text = models.CharField(verbose_name='Title', max_length=100, blank=True)
    organization_name = models.CharField(max_length=100, blank=True)
    address_line1 = models.CharField(max_length=45, blank=True)
    address_line2 = models.CharField(max_length=45, blank=True)
    city = models.ForeignKey(City)
    main_phone_number = models.CharField(max_length=25,blank=True)
    main_fax_number = models.CharField(max_length=25,blank=True)
    email = models.CharField(max_length=100,blank=True)


    @property
    def properties(self):
        return self.property_set.count()

    @property
    def total_units(self):
        return sum([p.property_total_unit_count for p in self.property_set.all()])

    def __unicode__(self):
        if self.individual_full_name:
            return self.individual_full_name
        else:
            return self.organization_name


class Property(models.Model):
    property_id = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0, editable=False)
    hub_name = models.CharField(max_length=30, blank=True)
    servicing_site_name = models.CharField(max_length=40, blank=True)
    name = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=25, blank=True)
    address_line1 = models.CharField(db_column=u'address_line1_text', verbose_name='Address Line 1',
                                     max_length=45, blank=True)
    address_line2 = models.CharField(db_column=u'address_line2_text', verbose_name='Address Line 2',
                                     max_length=45, blank=True)

    city = models.ForeignKey(City)

    msa_code = models.CharField(max_length=4, blank=True)
    msa_name = models.CharField(max_length=45, blank=True)

    congressional_district_code = models.CharField(max_length=15, blank=True)
    placed_base_city_name_text = models.CharField(max_length=30, blank=True)

    property_total_unit_count = models.DecimalField(verbose_name='Total Units', null=True, max_digits=8,
                                                    decimal_places=0, blank=True)
    property_category_name = models.CharField(verbose_name='Category',max_length=60, blank=True)
    primary_financing_type = models.CharField(max_length=30, blank=True)
    associated_financing_number = models.CharField(max_length=255, db_column=u'associated_financing_Number', blank=True)
    is_insured_ind = models.CharField(max_length=1, blank=True)
    is_202_811_ind = models.CharField(max_length=1, blank=True)
    is_hud_held_ind = models.CharField(max_length=1, blank=True)
    is_hud_owned_ind = models.CharField(max_length=1, blank=True)
    is_hospital_ind = models.CharField(max_length=1, blank=True)
    is_nursing_home_ind = models.CharField(max_length=1, blank=True)
    is_board_and_care_ind = models.CharField(max_length=1, blank=True)
    is_assisted_living_ind = models.CharField(max_length=1, blank=True)
    is_refinanced_ind = models.CharField(max_length=1, blank=True)
    is_221d3_ind = models.CharField(max_length=1, blank=True)
    is_221d4_ind = models.CharField(max_length=1, blank=True)
    is_236_ind = models.CharField(max_length=1, blank=True)
    is_non_insured_ind = models.CharField(max_length=1, blank=True)
    is_bmir_ind = models.CharField(max_length=1, blank=True)
    is_risk_sharing_ind = models.CharField(max_length=1, blank=True)
    is_mip_ind = models.CharField(max_length=1, blank=True)
    is_co_insured_ind = models.CharField(max_length=1, blank=True)

    ownership_effective_date = models.CharField(max_length=255, blank=True)

    owner = models.ForeignKey(Owner)
    management_agent = models.ForeignKey(ManagementAgent)

    class Meta:
        verbose_name_plural = _("Properties")

    def __unicode__(self):
        return self.name


class Properties_Contracts(models.Model):
    hub_name_text = models.CharField(max_length=30, blank=True)
    servicing_site_name_text = models.CharField(max_length=40, blank=True)
    property_id = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    property_name_text = models.CharField(max_length=50, blank=True)
    property_phone_number = models.CharField(max_length=25, blank=True)
    address_line1_text = models.CharField(max_length=45, blank=True)
    address_line2_text = models.CharField(max_length=45, blank=True)

    city_name_text = models.CharField(max_length=28, blank=True)
    state_code = models.CharField(max_length=2, blank=True)
    zip_code = models.CharField(max_length=5, blank=True)
    zip4_code = models.CharField(max_length=4, blank=True)

    county_code = models.CharField(max_length=3, blank=True)
    county_name_text = models.CharField(max_length=30, blank=True)

    msa_code = models.CharField(max_length=4, blank=True)
    msa_name_text = models.CharField(max_length=45, blank=True)

    congressional_district_code = models.CharField(max_length=15, blank=True)
    placed_base_city_name_text = models.CharField(max_length=30, blank=True)

    property_total_unit_count = models.DecimalField(null=True, max_digits=8, decimal_places=0, blank=True)
    property_category_name = models.CharField(max_length=60, blank=True)
    primary_financing_type = models.CharField(max_length=30, blank=True)
    associated_financing_number = models.CharField(max_length=255, db_column=u'associated_financing_Number', blank=True)
    is_insured_ind = models.CharField(max_length=1, blank=True)
    is_202_811_ind = models.CharField(max_length=1, blank=True)
    is_hud_held_ind = models.CharField(max_length=1, blank=True)
    is_hud_owned_ind = models.CharField(max_length=1, blank=True)
    is_hospital_ind = models.CharField(max_length=1, blank=True)
    is_nursing_home_ind = models.CharField(max_length=1, blank=True)
    is_board_and_care_ind = models.CharField(max_length=1, blank=True)
    is_assisted_living_ind = models.CharField(max_length=1, blank=True)
    is_refinanced_ind = models.CharField(max_length=1, blank=True)
    is_221d3_ind = models.CharField(max_length=1, blank=True)
    is_221d4_ind = models.CharField(max_length=1, blank=True)
    is_236_ind = models.CharField(max_length=1, blank=True)
    is_non_insured_ind = models.CharField(max_length=1, blank=True)
    is_bmir_ind = models.CharField(max_length=1, blank=True)
    is_risk_sharing_ind = models.CharField(max_length=1, blank=True)
    is_mip_ind = models.CharField(max_length=1, blank=True)
    is_co_insured_ind = models.CharField(max_length=1, blank=True)

    ownership_effective_date = models.CharField(max_length=255, blank=True)
    owner_participant_id = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    owner_company_type = models.CharField(max_length=20, blank=True)
    owner_individual_first_name = models.CharField(max_length=18, blank=True)
    owner_individual_middle_name = models.CharField(max_length=18, blank=True)
    owner_individual_last_name = models.CharField(max_length=20, blank=True)
    owner_individual_full_name = models.CharField(max_length=60, blank=True)
    owner_individual_title_text = models.CharField(max_length=100, blank=True)
    owner_organization_name = models.CharField(max_length=100, blank=True)
    owner_address_line1 = models.CharField(max_length=45, blank=True)
    owner_address_line2 = models.CharField(max_length=45, blank=True)
    owner_city_name = models.CharField(max_length=28, blank=True)
    owner_state_code = models.CharField(max_length=2, blank=True)
    owner_zip_code = models.CharField(max_length=5, blank=True)
    owner_zip4_code = models.CharField(max_length=4, blank=True)
    owner_main_phone_number_text = models.CharField(max_length=25, blank=True)
    owner_main_fax_number_text = models.CharField(max_length=25, blank=True)
    owner_email_text = models.CharField(max_length=100, blank=True)

    mgmt_agent_participant_id = models.DecimalField(null=True, max_digits=10, decimal_places=0, blank=True)
    mgmt_agent_company_type = models.CharField(max_length=20, blank=True)
    mgmt_agent_indv_first_name = models.CharField(max_length=18, blank=True)
    mgmt_agent_indv_last_name = models.CharField(max_length=18, blank=True)
    mgmt_agent_indv_middle_name = models.CharField(max_length=18, blank=True)
    mgmt_agent_full_name = models.CharField(max_length=56, blank=True)
    mgmt_agent_indv_title_text = models.CharField(max_length=100, blank=True)
    mgmt_agent_org_name = models.CharField(max_length=100, blank=True)
    mgmt_agent_address_line1 = models.CharField(max_length=45, blank=True)
    mgmt_agent_address_line2 = models.CharField(max_length=45, blank=True)
    mgmt_agent_city_name = models.CharField(max_length=28, blank=True)
    mgmt_agent_state_code = models.CharField(max_length=2, blank=True)
    mgmt_agent_zip_code = models.CharField(max_length=5, blank=True)
    mgmt_agent_zip4_code = models.CharField(max_length=4, blank=True)
    mgmt_agent_main_phone_number = models.CharField(max_length=25, blank=True)
    mgmt_agent_main_fax_number = models.CharField(max_length=18, blank=True)
    mgmt_agent_email_text = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = u'Properties_Contracts'

    def __unicode__(self):
        return self.hub_name_text
