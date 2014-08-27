from five import grok

from zope import schema
from plone.supermodel import model
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from scenario import IScenario
from driver import IDriver


from leam.luc import MessageFactory as _


# Interface class; used to define content-type schema.

class IDriverSet(model.Schema):
    """
    Computes population and employment changes per TAZ based on LEAM input.
    """
    year = schema.Int(
        title = _(u"Effective Year"),
        required = True,
        default = 2010,
    )

    trans = RelationChoice(
        title=_(u"trans"),
        source = ObjPathSourceBinder(
                object_provides=IDriver.__identifier__),
        required = True,
    )



# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class DriverSet(Container):
    grok.implements(IDriverSet)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# driver_set_templates
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IDriverSet)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
