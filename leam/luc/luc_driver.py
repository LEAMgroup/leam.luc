from five import grok

from z3c.form import group, field
from plone.supermodel import model
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder


from leam.luc import MessageFactory as _


drivers = SimpleVocabulary([
    SimpleTerm(value="area", title=_(u"area")),
    SimpleTerm(value="popdens", title=_(u"Population Density")),
    SimpleTerm(value="empdens", title=_(u"Employment Density")),
    SimpleTerm(value="roads", title=_(u"Road Network")),
    SimpleTerm(value="tdm", title=_(u"Travel Demand Modeled (TDM) Roads")),
    SimpleTerm(value="transit", title=_(u"Public Transit Network")),
    SimpleTerm(value="popcenter", title=_(u"Population Centers")),
    SimpleTerm(value="empcenter", title=_(u"Employment Centers")),
    SimpleTerm(value="special", title=_(u"Special Driver")),
    SimpleTerm(value="nogrowth", title=_(u"No Growth Zones")),
    SimpleTerm(value="landuse", title=_(u"Land Use and Land Cover")),
    SimpleTerm(value="dem", title=_(u"Elevation")),
    ])

# Interface class; used to define content-type schema.

class ILUCDriver(model.Schema):
    """
    A development driver for the LUC model.
    """

    title = schema.TextLine(
            title = _(u"Driver Title"),
        )

    description = schema.Text(
            title = _(u"Driver Description"),
        )

    year = schema.TextLine(
            title = _(u"Effective Year"),
        )

    layer = NamedBlobFile(
            title = _(u"GIS Layer"),
        )

    mapfile = NamedBlobFile(
            title = _(u"MapFile"),
            required = False,
        )

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class LUCDriver(Container):
    grok.implements(ILUCDriver)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# luc_driver_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(ILUCDriver)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
