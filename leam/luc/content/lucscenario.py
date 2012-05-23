"""Definition of the LUC Scenario content type
"""
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring
from Products.CMFCore.utils import getToolByName

from zope.interface import implements
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from archetypes.referencebrowserwidget import ReferenceBrowserWidget

# -*- Message Factory Imported Here -*-
from leam.luc import lucMessageFactory as _

from leam.luc.interfaces import ILUCScenario,ILUCSettings,IModel
from leam.luc.config import PROJECTNAME

LUCScenarioSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.ReferenceField(
        'growth',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            allow_browse=1,
            allow_search=0,
            startup_directory='/luc/projections',
            label=_(u"Growth Projections"),
            description=_(u"Identify one or more growth projection."),
        ),
        required=False,
        relationship='lucscenario_growth',
        allowed_types=('Projection'),
        multiValued=True,
    ),


    atapi.ReferenceField(
        'growthmap',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            allow_browse=1,
            allow_search=0,
            startup_directory='/luc/drivers',
            label=_(u"Growth Drivers"),
            description=_(u"Identify one or more sets of drivers."),
        ),
        required=False,
        relationship='lucscenario_growthmap',
        allowed_types=('Driver Set'),
        multiValued=True,
    ),


    atapi.ReferenceField(
        'decline',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            allow_browse=1,
            allow_search=0,
            startup_directory='/luc/projections',
            label=_(u"Vacancy Projections"),
            description=_(u"Add as many subregional projections as needed."),
        ),
        required=False,
        relationship='lucscenario_decline',
        allowed_types=('Projection'),
        multiValued=True,
    ),

    atapi.ReferenceField(
        'declinemap',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            allow_browse=1,
            allow_search=0,
            startup_directory='/luc/drivers',
            label=_(u"Vacancy Drivers"),
            description=_(u"Identify one or more sets of drivers."),
        ),
        required=False,
        relationship='lucscenario_declinemap',
        allowed_types=('Driver Set'),
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
        default="queued",
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
    implements(ILUCScenario, IModel)

    meta_type = "LUCScenario"
    schema = LUCScenarioSchema
    security = ClassSecurityInfo()

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    end_time = atapi.ATFieldProperty('end_time')

    start_time = atapi.ATFieldProperty('start_time')

    runstatus = atapi.ATFieldProperty('runstatus')

    growth = atapi.ATReferenceFieldProperty('growth')

    growthmap = atapi.ATReferenceFieldProperty('growthmap')

    decline = atapi.ATReferenceFieldProperty('decline')

    declinemap = atapi.ATReferenceFieldProperty('declinemap')


    security.declarePublic('requeue')
    def requeue(self):
        """simple method to requeue the scenario"""
        self.runstatus = 'queued'
        self.reindexObject(['runstatus',])
        return "requeue"


    security.declarePublic('end_run')
    def end_run(self):
        """Mark the run as complete, set the end time, and set
           default page to summary.
           NEEDS WORK -- should set the endtime field, should set the
           default page to the summary doc, should pass an arg that 
           selects 'complete' or 'terminated'.
           
           more on setDefaultPage at https://svn.plone.org/svn/collective/CMFDynamicViewFTI/trunk/Products/CMFDynamicViewFTI/interfaces.py#L84
        """
        #import pdb; pdb.set_trace()
        self.runstatus = 'complete'
        self.reindexObject(['runstatus',])
        
        #self.setDefaultPage(obj)
        return
        

    security.declarePublic('getConfig')
    def getConfig(self):
        """Returns the cconfiguration necessary for running the model"""
        #import pdb; pdb.set_trace()

        model = Element('model')
        tree = SubElement(model, 'scenario')
        SubElement(tree, 'id').text = self.id
        SubElement(tree, 'title').text = self.title
        SubElement(tree, 'results').text = self.absolute_url()

        # get the repository from registry 
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ILUCSettings)
        SubElement(tree, 'repository').text = settings.scenario_repo
        SubElement(tree, 'cmdline').text = settings.scenario_cmd

        # regions to be modeled
        reg = SubElement(tree, 'growth')
        for p in self.getGrowth():
            reg.append(fromstring(p.getConfig()))
        reg = SubElement(tree, 'growthmap')
        for p in self.getGrowthmap():
            reg.append(fromstring(p.getConfig()))

        reg = SubElement(tree, 'decline')
        for p in self.getDecline():
            reg.append(fromstring(p.getConfig()))
        reg = SubElement(tree, 'declinemap')
        for p in self.getDeclinemap():
            reg.append(fromstring(p.getConfig()))

        reg = SubElement(tree, 'postprocess')
        #urltool = getToolByName(self.context, 'portal_url')
        #portal = urltool.getPortalObject()
        #zones = portal.luc.scenarios.subarearesults
        #for p in zones.values():
        #    SubElement(reg, 'zones').text = p.absolute_url() + \
        #        '/at_download/simImage'

        self.REQUEST.RESPONSE.setHeader('Content-Type',
            'application/xml;;charset=UTF-8')
        self.REQUEST.RESPONSE.setHeader('Content-Disposition',
            'attachment; filename="%s_scenario.xml"' % self.title)
        return tostring(model, encoding='UTF-8')


atapi.registerType(LUCScenario, PROJECTNAME)
