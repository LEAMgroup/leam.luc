from xml.etree.ElementTree import Element, tostring

from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from leam.luc import lucMessageFactory as _
from leam.luc.interfaces import IModel


class IPopQueue(Interface):
    """
    project view interface
    """
    pass


class PopQueue(BrowserView):
    """
    project browser view
    """
    implements(IPopQueue)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def __call__(self):
        
        #import pdb; pdb.set_trace()

        filter = { 'object_provides' : IModel.__identifier__,
                   'runstatus' : 'queued'
                 }

        results = self.portal_catalog(filter, sort_on='modified')
        if results:
            try:
                config = self.context.restrictedTraverse(
                    results[0].getPath() + '/getConfig')
                ret = config()

            except Exception:
                results[0].getObject().setRunstatus('error')
                results[0].getObject().reindexObject(['runstatus',])

                ret = Element('queue')                
                ret.text = "ERROR"
                self.request.RESPONSE.setHeader('Content-Type', 
                    'application/xml;;charset=UTF-8')
                return tostring(ret, encoding='UTF-8')

            # return configuration
            results[0].getObject().setRunstatus('running')
            results[0].getObject().reindexObject(['runstatus',])
            return ret

        else:
            ret = Element('queue')
            ret.text = "EMPTY"
            self.request.RESPONSE.setHeader('Content-Type', 
                'application/xml;;charset=UTF-8')
            return tostring(ret, encoding='UTF-8')

