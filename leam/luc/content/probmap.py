"""Definition of the Probmap content type
"""
from xml.etree.ElementTree import Element, SubElement
from xml.etree.ElementTree import tostring, fromstring

from zope.interface import implements

from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from plone.app.blob.field import BlobField
from archetypes.referencebrowserwidget import ReferenceBrowserWidget

# -*- Message Factory Imported Here -*-
from leam.luc import lucMessageFactory as _

from leam.luc.interfaces import IProbmap
from leam.luc.config import PROJECTNAME

ProbmapSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.IntegerField(
        'year',
        storage=atapi.AnnotationStorage(),
        widget=atapi.IntegerWidget(
            label=_(u"Effective Year"),
            description=_(u"First year the probmap will be used. Each driver given below should coorespond to this year."),
        ),
        required=True,
        default=_(u"2010"),
        validators=('isInt'),
    ),


    atapi.ReferenceField(
        'tdm',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            allow_browse=1,
            allow_search=1,
            startup_directory='/luc/transportation',
            label=_(u"Travel Demand Model Transportation Network"),
            description=_(u"Select a transportation network that has been generated from a travel demand model."),
        ),
        required=True,
        relationship='probmap_tdm',
        allowed_types=('SimMap'),
        multiValued=False,
    ),


    atapi.ReferenceField(
        'roads',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            allow_browse=1,
            allow_search=1,
            startup_directory='/luc/transportation',
            label=_(u"Additional Roads"),
            description=_(u"Select a GIS layer that contains any roads not included in the TDM network."),
        ),
        relationship='probmap_roads',
        allowed_types=('SimMap'),
        multiValued=False,
    ),


#    atapi.ReferenceField(
#        'transit',
#        storage=atapi.AnnotationStorage(),
#        widget=ReferenceBrowserWidget(
#            visible={'view': 'hidden', 'edit': 'hidden'},
#            allow_browse=1,
#            allow_search=1,
#            startup_directory='/luc/transportation',
#
#            label=_(u"Transit Networks"),
#            description=_(u"Select one or more GIS layers containing regional or local transit networks."),
#        ),
#        relationship='probmap_transit',
#        allowed_types=('SimMap'),
#        multiValued=True,
#    ),


    atapi.ReferenceField(
        'drivers',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            allow_browse=1,
            allow_search=1,
            startup_directory='/luc/specials',
            label=_(u"Zonal Drivers"),
            description=_(u"Select one or more GIS layers.  Drivers modify the probability map in the uniform way."),
        ),
        relationship='probmap_driver',
        allowed_types=('SimMap'),
        multiValued=True,
    ),


    atapi.ReferenceField(
        'nogrowth',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            allow_browse=1,
            allow_search=1,
            startup_directory='/luc/nogrowth',
            label=_(u"No Growth Maps"),
            description=_(u"Select one or more GIS layers.  These areas will be protected from model development."),
        ),
        relationship='probmap_nogrowth',
        allowed_types=('SimMap'),
        multiValued=True,
    ),


    atapi.ReferenceField(
        'popcenters',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"City and Population Centers"),
            description=_(u"Select the GIS layer with city centers."),
            startup_directory='/luc/attractors',
        ),
        required=True,
        relationship='probmap_popcenters',
        allowed_types=('SimMap'), # specify portal type names here ('Example Type',)
        multiValued=True,
    ),


    atapi.ReferenceField(
        'empcenters',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"Employment Centers"),
            description=_(u"Select a GIS layer containing employeers and employmment centers."),
            startup_directory='/luc/attractors',
        ),
        required=True,
        relationship='probmap_empcenters',
        allowed_types=('SimMap'),
        multiValued=True,
    ),


    atapi.ReferenceField(
        'landuse',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"Initial Land Use Map"),
            description=_(u"Provide an initial land use map for the scenario.  Unused if a Starting Scenario is provided."),
            startup_directory='/luc/grids',
        ),
        required=True,
        relationship='probmap_landuse',
        allowed_types=('SimMap'),
        multiValued=False,
    ),


    atapi.ReferenceField(
        'dem',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"Digital Elevation Map"),
            description=_(u"Select a GIS layer that provides regional elevation."),
            startup_directory='/luc/grids',
        ),
        required=True,
        relationship='probmap_dem',
        allowed_types=('SimMap'),
        multiValued=False,
    ),


    atapi.ReferenceField(
        'probview',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"Probmap View"),
            description=_(u"A SimMap view visualzing the Probmap."),
            startup_directory='/luc/probmaps',
        ),
        relationship='probmap_probview',
        allowed_types=('SimMap'),
        multiValued=False,
    ),


    BlobField(
        'probfile',
        storage=atapi.AnnotationStorage(),
        widget=atapi.FileWidget(
            label=_(u"Probmap File"),
            description=_(u"Precomputed version of the probability map."),
        ),
        required=False,
    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

ProbmapSchema['title'].storage = atapi.AnnotationStorage()
ProbmapSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(ProbmapSchema, moveDiscussion=False)


class Probmap(base.ATCTContent):
    """a Land Use Change probability map"""
    implements(IProbmap)

    meta_type = "Probmap"
    schema = ProbmapSchema
    security = ClassSecurityInfo()

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    year = atapi.ATFieldProperty('year')

    roads = atapi.ATReferenceFieldProperty('roads')

    #transit = atapi.ATReferenceFieldProperty('transit')

    tdm = atapi.ATReferenceFieldProperty('tdm')

    drivers = atapi.ATReferenceFieldProperty('drivers')

    nogrowth = atapi.ATReferenceFieldProperty('nogrowth')

    empcenters = atapi.ATReferenceFieldProperty('empcenters')

    popcenters = atapi.ATReferenceFieldProperty('popcenters')

    dem = atapi.ATReferenceFieldProperty('dem')

    landuse = atapi.ATReferenceFieldProperty('landuse')

    probview = atapi.ATReferenceFieldProperty('probview')

    probfile = atapi.ATFieldProperty('probfile')


    security.declarePublic('getConfig')
    def getConfig(self):
        """Generate a configuration file for the Probmap"""

        tree = Element('probmap')

        tag = SubElement(tree, 'title')
        tag.text = self.title
        tag = SubElement(tree, 'tdm')
        tag.text = self.tdm.absolute_url() + '/get_layer'
        tag = SubElement(tree, 'roads')
        tag.text = self.roads.absolute_url() + '/get_layer'

        tags = SubElement(tree, 'drivers')
        for s in self.drivers:
            tag = SubElement(tags, 'driver')
            tag.text = s.absolute_url() + '/get_layer'
        
        tags = SubElement(tree, 'nogrowth_maps')
        for s in self.nogrowth:
            tag = SubElement(tags, 'nogrowth')
            tag.text = s.absolute_url() + '/get_layer'
        
        tags = SubElement(tree, 'empcenters')
        for s in self.empcenters:
            tag = SubElement(tags, 'empcenter')
            tag.text = s.absolute_url() + '/get_layer'
        
        tags = SubElement(tree, 'popcenters')
        for s in self.popcenters:
            tag = SubElement(tags, 'popcenter')
            tag.text = s.absolute_url() + '/get_layer'

        tag = SubElement(tree, 'landuse')
        tag.text = self.landuse.absolute_url() + '/get_layer'
        tag = SubElement(tree, 'dem')
        tag.text = self.dem.absolute_url() + '/get_layer'

        if self.probfile:
            tag = SubElement(tree, 'probfile')
            tag.text = self.probfile.absolute_url() + '/at_download'

        self.REQUEST.RESPONSE.setHeader('Content-Type',
            'application/xml;;charset=UTF-8')
        self.REQUEST.RESPONSE.setHeader('Content-Disposition',
            'attachment; filename="%s_probmap.xml"' % self.title)

        return tostring(tree, encoding='UTF-8')


atapi.registerType(Probmap, PROJECTNAME)
