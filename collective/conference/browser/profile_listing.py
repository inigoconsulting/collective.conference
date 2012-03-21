from five import grok
from collective.conference.conference import IConference
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class ParticipantListView(grok.View):
    grok.context(IConference)
    grok.template('profile_listing')
    grok.name('participants')
    grok.require('zope2.View')

    title = u"Participants"

    def items(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog({
            'portal_type': 'collective.conference.participant',
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 2
            },
            'sort_on':'sortable_title'
        })
        return [i.getObject() for i in brains]
