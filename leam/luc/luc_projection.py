from five import grok

from z3c.form import group, field
from plone.supermodel import model
from zope import schema
from zope.interface import Interface, invariant, Invalid
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

from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow


from leam.luc import MessageFactory as _

devtypes = SimpleVocabulary([
    SimpleTerm(value='growth', title=_(u"New Growth")),
    SimpleTerm(value='redev', title=_(u"Redevelopment")),
    SimpleTerm(value='vacancy', title=_(u"Vacancy and Abandonment")),
    ])

class IProjectionRow(Interface):
    """grid table for population and employment projections"""
    year = scheme.TextLine(title=_(u"Year"))
    pop = scheme.TextLine(title=_(u"Population"))
    emp = scheme.TextLine(title=_(u"Employment"))

# Interface class; used to define content-type schema.

class ILUCProjection(model.Schema):
    """
    A region and population/employment projection for the LUC model.
    """

    title = schema.TextLine(
            title=_(u"Projection Name"),
        )

    description = schema.Text(
            title=_(u"Projection Summary"),
        )

    proj = schema.List(
            title=_(u"Projection"),
            value_type=DictRow(title=u"projrow", schema=IProjectionRow),
        )

    devtype = schema.Choice(
            title=_(u"Development Type"),
            vocabulary=devtypes,
            default="growth",
        )

    area = RelationChoice(
            title=_(u"Effective Area"),
        )

    popdens = RelationChoice(
            title=_(u"Population Density"),
            description=_(u"Future population density driver (required for "
                          u"regional projections)"),
            required = False,
        )

    empdens = RelationChoice(
            title=_(u"Employment Density"),
            description=_(u"Future employment density driver (required for "
                          u"regional projections)"),
            required = False,
        )
                 
    drivers = RelationList(
            title=_(u"Driver Sets"),
            description=_(u"Driver Sets used during model (required for "
                          u"regional projections)"),
            required=False,
        )

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class LUCProjection(Container):
    grok.implements(ILUCProjection)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# luc_projection_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(ILUCProjection)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
