# from django.db import models
# Import separately
from django.contrib.gis.db import models # defines geometry field types
from django.contrib.auth.models import User # refers to auth_user table
from django.template.defaultfilters import escape
from django.core.urlresolvers import reverse

# django-cms imports
from cms.models import CMSPlugin

# Python imports
from datetime import datetime

# Create your models here.

class Organisations(models.Model):
    ORG_CATS = (
        (u'school', u'School'),
        (u'ngo', u'NGO'),
        (u'conservancy', u'Conservancy'),
        (u'private', u'Private citizen'),
        (u'government', u'Government department')
    )
    org_name = models.CharField(max_length=100, blank=True)
    org_type = models.CharField(max_length=11, choices=ORG_CATS, blank=True)

    class Meta:
        db_table = u'organisations'

    def __unicode__(self):
        return self.org_name

class Schools(models.Model):
    gid = models.AutoField(primary_key=True, editable=False)
    the_geom = models.PointField()
    natemis = models.IntegerField()
    school = models.CharField(max_length=255)
    province = models.CharField(max_length=2)
    phase = models.CharField(max_length=12)
    objects = models.GeoManager()

    class Meta:
        db_table = u'schools'
        managed=False

    def __unicode__(self):
        return self.name

class Sites(models.Model):
    RIVER_CATS = (
        (u'rocky', u'Rocky'),
        (u'sandy', u'Sandy')
    )
    gid = models.AutoField(primary_key=True, editable=False)
    the_geom = models.PointField()
    site_name = models.CharField(max_length=15, blank=False)
    river_name = models.CharField(max_length=15, blank=False)
    description = models.CharField(max_length=255, blank=True)
    river_cat = models.CharField(max_length=5, choices=RIVER_CATS, blank=True)
    user = models.ForeignKey(User)
    time_stamp = models.DateTimeField(auto_now=True, auto_now_add=True)
    objects = models.GeoManager()

    class Meta:
        db_table = u'sites'

    def __unicode__(self):
        return self.site_name

class Observations(models.Model):
    FLAG_CATS = (
        (u'dirty', u'Dirty'),
        (u'clean', u'Clean')
    )
    UNIT_DO_CATS = (
        (u'mgl', u'mg/l'),
        (u'pDO', u'%DO'),
        (u'na', u'Unknown')
    )
    UNIT_EC_CATS = (
        (u'mSm', u'mS/m'),
        (u'na', u'Unknown')
    )
    gid = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User)
    flatworms = models.BooleanField(default=False)
    worms = models.BooleanField(default=False)
    leeches = models.BooleanField(default=False)
    crabs_shrimps = models.BooleanField(default=False)
    stoneflies = models.BooleanField(default=False)
    minnow_mayflies = models.BooleanField(default=False)
    other_mayflies = models.BooleanField(default=False)
    damselflies = models.BooleanField(default=False)
    dragonflies = models.BooleanField(default=False)
    bugs_beetles = models.BooleanField(default=False)
    caddisflies = models.BooleanField(default=False)
    true_flies = models.BooleanField(default=False)
    snails = models.BooleanField(default=False)
    score = models.DecimalField(max_digits=4, decimal_places=2)
    site = models.ForeignKey(Sites, db_column='site',related_name='observation')
    time_stamp = models.DateTimeField(auto_now=True, auto_now_add=True)
    comment = models.CharField(max_length=255, blank=True)
    obs_date = models.DateField()
    flag = models.CharField(max_length=5, choices=FLAG_CATS, default='dirty', blank=False)
    water_clarity = models.DecimalField(max_digits=8, decimal_places=1, blank=True)
    water_temp = models.DecimalField(max_digits=5, decimal_places=1, blank=True)
    ph = models.DecimalField(max_digits=4, decimal_places=1, blank=True)
    diss_oxygen = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    diss_oxygen_unit = models.CharField(max_length=8, choices=UNIT_DO_CATS, default='mgl', blank=True)
    elec_cond = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    elec_cond_unit = models.CharField(max_length=8, choices=UNIT_EC_CATS, default='mSm', blank=True)
    objects = models.GeoManager()

    class Meta:
        db_table = u'observations'

    def __unicode__(self):
        return str(self.obs_date) + ': ' + self.site.site_name

class ObservationPlugin(CMSPlugin):
    """ This is a Django CMS plugin for the above Observations monitor model class
    """
#     observation = models.ForeignKey(Observations, related_name='plugins')
#
#     def __unicode__(self):
#         return self.observation.site.name
