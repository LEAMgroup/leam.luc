"""Definition of the LUC Scenario content type
"""
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring

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
        allowed_types=('Projection'),
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
        'start_time',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Start Time"),
            description=_(u"When the model began execution."),
            visible={'view': 'hidden', 'edit': 'hidden'},
        ),
        validators=('isValidDate'),
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

    atapi.StringField(
        'gis',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"GIS repository"),
            description=_(u"a predefined GRASS location used by the model"),
            visible={'view': 'hidden', 'edit': 'hidden'},
        ),
        required=True,
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
    merge = atapi.ATReferenceFieldProperty('merge')

    probmaps = atapi.ATReferenceFieldProperty('probmaps')

    gis = atapi.ATFieldProperty('gis')

    cmdline = atapi.ATFieldProperty('cmdline')

    repository = atapi.ATFieldProperty('repository')

    end_time = atapi.ATFieldProperty('end_time')

    start_time = atapi.ATFieldProperty('start_time')

    runstatus = atapi.ATFieldProperty('runstatus')

    subregions = atapi.ATReferenceFieldProperty('subregions')

    region = atapi.ATReferenceFieldProperty('region')


    security.declarePublic('requeue')
    def requeue(self):
        """simple method to requeue the scenario"""
        self.runstatus = 'queued'
        self.reindexObject(['runstatus',])

    security.declarePublic('getConfig')
    def getConfig(self):
        """Returns the cconfiguration necessary for running the model"""
        #import pdb; pdb.set_trace()

        tree = Element('model')
        tag = SubElement(tree, 'title')
        tag.text = self.title

        # model startup
        tag = SubElement(tree, 'repository')
        tag.text = self.getRepository()
        tag = SubElement(tree, 'cmdline')
        tag.text = self.getCmdline()

        # regions to be modeled
        tree.append(fromstring(self.getRegion().getConfig()))
        reg = SubElement(tree, 'subregions')
        for p in self.getSubregions():
            reg.append(fromstring(p.getConfig()))

        # current scenario for results
        tag = SubElement(tree, 'results')
        tag.text = self.absolute_url()
        
        self.REQUEST.RESPONSE.setHeader('Content-Type',
            'application/xml;;charset=UTF-8')
        self.REQUEST.RESPONSE.setHeader('Content-Disposition',
            'attachment; filename="%s_scenario.xml"' % self.title)
        return tostring(tree, encoding='UTF-8')


atapi.registerType(LUCScenario, PROJECTNAME)
