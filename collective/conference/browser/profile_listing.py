from five import grok
from collective.conference.conference import IConference
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class SpeakerListView(grok.View):
    grok.context(IConference)
    grok.template('profile_listing')
    grok.name('participants')

    title = u"Participants"

    def items(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog({
            'portal_type': 'collective.conference.participant',
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 2
            }
        })
        return [i.getObject() for i in brains]
