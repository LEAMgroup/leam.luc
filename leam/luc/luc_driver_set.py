from five import grok

from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Item
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from leam.simmap import ISimmap
from leam.luc import ILUCScenario

from leam.ewg_taz import MessageFactory as _


# Interface class; used to define content-type schema.

class ITAZAnalysis(form.Schema, IImageScaleTraversable):
    """
    Computes population and employment changes per TAZ based on LEAM input.
    """
    basemap = RelationChoice(
        title=_(u"TAZ Base Map"),
        source = ObjPathSourceBinder(object_provides=ISimmap.__identifier__),
        required = True,
    )

    year = schema.Int(
        title = _(u"TAZ Base Year"),
        required = True,
        default = 2010,
    )

    scenario = RelationChoice(
        title = _(u"LEAM Scenario"),
        source = ObjPathSourceBinder(
            object_provides=ILUCScenario.__identifier__),
        required = True,
    )

    results = schema.Boolean(
        title = _(u"Keep results with scenario"),
        default = True,
    )


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class TAZAnalysis(Item):
    grok.implements(ITAZAnalysis)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# taz_analysis_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(ITAZAnalysis)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
