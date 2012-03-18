from five import grok
from collective.conference.conference import IConference
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class SessionListView(grok.View):
    grok.context(IConference)
    grok.template('session_listing')
    grok.name('sessions')

    title = u"Sessions"

    def items(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog({
            'portal_type': 'collective.conference.session',
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 2
            },
            'sort_on':'sortable_title'
        })
        return [i.getObject() for i in brains]
