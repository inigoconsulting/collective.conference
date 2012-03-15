from five import grok
from collective.conference.conference import IConference
from collective.conference.participant import IParticipant
from collective.conference.session import ISession
from collective.conference.provider.listing import TableListingProvider
from plone.directives import form
from zope import schema
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class AttendeesListingView(grok.View):
    grok.context(IConference)
    grok.template('listing')
    grok.name('attendees')
    grok.require('cmf.ModifyPortalContent')

    title = 'Attendees listing'

    def provider(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog({
            'portal_type': 'collective.conference.participant',
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 2
            }
        })
        return TableListingProvider(self.request, IParticipant, [
            i.getObject() for i in brains
            ])


class VegetarianListingView(grok.View):
    grok.context(IConference)
    grok.template('listing')
    grok.name('vegetarians')
    grok.require('cmf.ModifyPortalContent')

    title = 'Vegetarians listing'

    def provider(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog({
            'portal_type': 'collective.conference.participant',
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 2
            }
        })
        objs = [ i.getObject() for i in brains ]
        return TableListingProvider(self.request, IParticipant, [
            i for i in objs if i.is_vegetarian
        ])


class ISessionList(form.Schema):

    title = schema.TextLine(
        title=u'Title'
    )

    session_type = schema.Choice(
        title=u'Session Type',
        vocabulary="collective.conference.vocabulary.sessiontype"
    )

    level = schema.Choice(
        title=u'Level',
        vocabulary="collective.conference.vocabulary.sessionlevel"
    )

    conference_rooms = schema.List(
        title=u'Conference Rooms',
        value_type=schema.TextLine()
    )


class SessionListingView(grok.View):
    grok.context(IConference)
    grok.template('listing')
    grok.name('sessions')
    grok.require('zope2.View')

    title = u'Submitted Sessions'

    def provider(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog({
            'portal_type': 'collective.conference.session',
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 2
            }
        })
        objs = [ i.getObject() for i in brains ]
        return TableListingProvider(self.request, ISessionList, objs)
