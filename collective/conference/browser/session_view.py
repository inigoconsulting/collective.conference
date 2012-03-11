from five import grok
from collective.conference.session import ISession
from collective.conference.conference import IConference
from Acquisition import aq_parent
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class SessionView(grok.View):
    grok.context(ISession)
    grok.name('session_view')
    grok.template('session_view')

    def roomName(self):
        return getattr(self.context, 'conferenceroom', None)

    def speakers(self):
        result = []
        emails = getattr(self.context, 'emails', [])
        if not emails:
            return []

        conference = self.getConference()
        catalog = getToolByName(self.context, 'portal_catalog')
        for p in catalog({
            'portal_type': 'collective.conference.participant',
            'path': {
                'query': '/'.join(conference.getPhysicalPath()),
                'depth': 3
            }
        }):
            obj = p.getObject()
            if obj.email in emails:
                result.append(obj)
        return result

    def getConference(self):
        site = getSite()
        parent = aq_parent(self.context)
        while parent != site:
            if IConference.providedBy(parent):
                return parent
            parent = aq_parent(parent)
        return None
