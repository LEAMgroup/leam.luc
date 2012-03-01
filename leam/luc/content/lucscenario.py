"""Definition of the LUC Scenario content type
"""
from xml.etree.ElementTree import Element, SubElement, tostring

from zope.interface import implements

from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from archetypes.referencebrowserwidget import ReferenceBrowserWidget

# -*- Message Factory Imported Here -*-
from leam.luc import lucMessageFactory as _

from leam.luc.interfaces import ILUCScenario
from leam.luc.config import PROJECTNAME

LUCScenarioSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-


    atapi.ReferenceField(
        'region',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            allow_browse=1,
            allow_search=0,
            startup_directory='/luc/projections',
            label=_(u"Regional Projection"),
            description=_(u"Identify the study area and a baseline population and employment projection."),
        ),
        required=True,
        relationship='lucscenario_region',
        allowed_types=('Projection'), # specify portal type names here ('Example Type',)
        multiValued=False,
    ),


    atapi.ReferenceField(
        'subregions',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            allow_browse=1,
            allow_search=0,
            startup_directory='/luc/projections',
            label=_(u"Sub-Regional Projections"),
            description=_(u"Add as many subregional projections as needed."),
        ),
        relationship='lucscenario_subregions',
        allowed_types=('Projection'),
        multiValued=True,
    ),


    atapi.ReferenceField(
        'starting_scenario',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            allow_browse=1,
            allow_search=1,
            label=_(u"Starting Scenario"),
            description=_(u"Select existing scenario if the new scenario will build upon previous model results."),
        ),
        relationship='lucscenario_starting_scenario',
        allowed_types=('LUCScenario'),
        multiValued=False,
    ),


    atapi.IntegerField(
        'syear',
        storage=atapi.AnnotationStorage(),
        widget=atapi.IntegerWidget(
            label=_(u"Starting Year"),
            description=_(u"Enter the starting year of the scenario."),
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
            allow_search=0,
            startup_directory='/luc/transportation',
            label=_(u"Travel Demand Model Transportation Network"),
            description=_(u"Select a transportation network that has been generated from a travel demand model."),
        ),
        required=True,
        relationship='lucscenario_tdm',
        allowed_types=('SimMap'),
        multiValued=False,
    ),


    atapi.ReferenceField(
        'roads',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            allow_browse=1,
            allow_search=0,
            startup_directory='/luc/transportation',
            label=_(u"Additional Roads"),
            description=_(u"Select a GIS layer that contains any roads not included in the TDM network."),
        ),
        relationship='lucscenario_roads',
        allowed_types=('SimMap'),
        multiValued=False,
    ),


    atapi.ReferenceField(
        'transit',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            allow_browse=1,
            allow_search=0,
            startup_directory='/luc/transportation',
            label=_(u"Transit Networks"),
            description=_(u"Select one or more GIS layers containing regional or local transite networks."),
        ),
        visible={'view': 'hidden', 'edit': 'hidden'},
        relationship='lucscenario_transit',
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
        relationship='lucscenario_nogrowth',
        allowed_types=('SimMap'),
        multiValued=True,
    ),


    atapi.ReferenceField(
        'landuse',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"Initial Land Use Map"),
            description=_(u"Provide an initial land use map for the scenario.  Unused if a Starting Scenario is provided."),
        ),
        required=True,
        relationship='lucscenario_landuse',
        allowed_types=('SimMap'),
        multiValued=False,
    ),


    atapi.ReferenceField(
        'popcenters',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"City and Population Centers"),
            description=_(u"Select the GIS layer with city centers."),
        ),
        required=True,
        relationship='lucscenario_popcenters',
        allowed_types=('SimMap'), # specify portal type names here ('Example Type',)
        multiValued=False,
    ),


    atapi.ReferenceField(
        'empcenters',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"Employment Centers"),
            description=_(u"Select a GIS layer containing employeers and employmment centers."),
        ),
        required=True,
        relationship='lucscenario_empcenter',
        allowed_types=('SimMap'),
        multiValued=False,
    ),


    atapi.ReferenceField(
        'dem',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"Digital Elevation Map"),
            description=_(u"Select a GIS layer that provides regional elevation."),
        ),
        required=True,
        relationship='lucscenario_dem',
        allowed_types=('SimMap'),
        multiValued=False,
    ),


    atapi.StringField(
        'runstatus',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Run Status"),
            description=_(u"Provide the current run state of the scenario."),
            visible={'view': 'hidden', 'edit': 'hidden'},
        ),
        required=True,
        default=_(u"queued"),
    ),


    atapi.DateTimeField(
        'end_time',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"End Time"),
            description=_(u"When the model completed."),
            visible={'view': 'hidden', 'edit': 'hidden'},
        ),
        validators=('isValidDate'),
    ),


    atapi.DateTimeField(
        'start_time',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Start Time"),
            description=_(u"When the model began execution."),
            visible={'view': 'hidden', 'edit': 'hidden'},
        ),
        validators=('isValidDate'),
    ),


    atapi.StringField(
        'cmdline',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Command line to begin execution after checkout of repository."),
            description=_(u"blah"),
            visible={'view': 'hidden', 'edit': 'hidden'},
        ),
        required=True,
        default=_(u"startup.py"),
    ),


    atapi.StringField(
        'repository',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Code Repository"),
            description=_(u"The subversion repository containing necessary run time files."),
            visible={'view': 'hidden', 'edit': 'hidden'},
        ),
        required=True,
        default=_(u"http://datacenter.leamgroup.com/svn/desktop/ewg_luc/trunk"),
    ),


))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

LUCScenarioSchema['title'].storage = atapi.AnnotationStorage()
LUCScenarioSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    LUCScenarioSchema,
    folderish=True,
    moveDiscussion=False
)


class LUCScenario(folder.ATFolder):
    """LEAM Land Use Change (LUC) Scenario"""
    implements(ILUCScenario)

    meta_type = "LUCScenario"
    schema = LUCScenarioSchema
    security = ClassSecurityInfo()

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    cmdline = atapi.ATFieldProperty('cmdline')

    repository = atapi.ATFieldProperty('repository')

    end_time = atapi.ATFieldProperty('end_time')

    start_time = atapi.ATFieldProperty('start_time')

    runstatus = atapi.ATFieldProperty('runstatus')

    roads = atapi.ATReferenceFieldProperty('roads')

    transit = atapi.ATReferenceFieldProperty('transit')

    tdm = atapi.ATReferenceFieldProperty('tdm')

    nogrowth = atapi.ATReferenceFieldProperty('nogrowth')

    empcenters = atapi.ATReferenceFieldProperty('empcenters')

    popcenters = atapi.ATReferenceFieldProperty('popcenters')

    dem = atapi.ATReferenceFieldProperty('dem')

    landuse = atapi.ATReferenceFieldProperty('landuse')

    syear = atapi.ATFieldProperty('syear')

    starting_scenario = atapi.ATReferenceFieldProperty('starting_scenario')

    subregions = atapi.ATReferenceFieldProperty('subregions')

    region = atapi.ATReferenceFieldProperty('region')

    security.declarePublic('getConfig')
    def getConfig(self):
        """Returns the cconfiguration necessary for running the model"""
        import pdb; pdb.set_trace()

        tree = Element('model')
        tag = SubElement(tree, 'title')
        tag.text = self.title

        # model startup
        tag = SubElement(tree, 'repository')
        tag.text = self.getRepository()
        tag = SubElement(tree, 'cmdline')
        tag.text = self.getCmdline()

        # regions to be modeled
        tag = SubElement(tree, 'region')
        tag.text = self.getRegion().absolute_url() + '/getGraph'
        reg = SubElement(tree, 'subregions')
        for p in self.getSubregions():
            tag = SubElement(reg, 'region')
            tag.text = p.absolute_url() + '/getGraph'

        tag = SubElement(tree,'starting_year')
        tag.text = self.getSyear()

        # setup Starting Scenario
        if self.getStarting_scenario():
            tag = SubElemennt(tree, 'starting_scenario')
            tag.text = self.getStarting_scenario().absolute_url()

        tag = SubElement(tree, 'tdm_network')
        tag.text = self.getTdm().absolute_url() + '/get_layer'
        tag = SubElement(tree, 'road_network')
        tag.text = self.getRoads().absolute_url() + '/get_layer'

        if self.getTransit():
            tag = SubElement(tree, 'transit_network')
            tag.text = self.getTransit().absolute_url() + '/get_layer'

        # setup nogrowth layers if any
        reg = SubElement(tree, 'no_growth_layers')
        for s in  self.getNogrowth():
            tag = SubElement(reg, 'no_growth')
            tag.text = s.absolute_url() + '/get_layer'

        # basic drivers
        tag = SubElement(tree, 'landuse')
        tag.text = self.getLanduse().absolute_url() + '/get_layer'

        tag = SubElement(tree, 'dem')
        tag.text = self.getDem().absolute_url() + '/get_layer'

        tag = SubElement(tree, 'popcenters')
        tag.text = self.getPopcenters().absolute_url() + '/get_layer'

        tag = SubElement(tree, 'empcenters')
        tag.text = self.getEmpcenters().absolute_url() + '/get_layer'

        # current scenario for results
        tag = SubElement(tree, 'results')
        tag.text = self.absolute_url()
        
        
        self.REQUEST.RESPONSE.setHeader('Content-Type', 'application/xml')
        return tostring(tree)
        


atapi.registerType(LUCScenario, PROJECTNAME)
