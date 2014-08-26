import json

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
            obj = results[0].getObject()
            url = obj.absolute_url()
            rsp = dict(
                status = 'OK',
                id = obj.id,
                title = obj.title,
                url = url,
                config = url + '/getConfig',
                on_done = url + '/run_complete',
                )

            try:
                rsp['repository'] = obj.getRepository(obj)
            except AttributeError:
                rsp['repository'] = ''

            try:
                rsp['cmdline'] = obj.getCmdline(obj)
            except AttributeError:
                rsp['cmdline'] = ''

            # mark the object as running
            obj.runstatus = 'running'
            obj.reindexObject(['runstatus',])

        # nothing to do
        else:
            rsp = dict( status = 'EMPTY' )

        self.request.RESPONSE.setHeader('Content-Type', 'application/json')
        return json.dumps(rsp)

