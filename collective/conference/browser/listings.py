from five import grok
from collective.conference.conference import IConference
from collective.conference.participant import IParticipant
from collective.conference.session import ISession
from collective.conference.provider.listing import TableListingProvider
from plone.directives import form
from zope import schema
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class IParticipantList(IParticipant):
    form.omitted('description')

class AttendeesListingView(grok.View):
    grok.context(IConference)
    grok.template('listing')
    grok.name('participant-list')
    grok.require('cmf.ModifyPortalContent')

    title = 'Attendees listing'

    def provider(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog({
            'portal_type': 'collective.conference.participant',
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 2
            },
            'sort_on':'created'
        })
        return TableListingProvider(self.request, IParticipantList, [
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
        return TableListingProvider(self.request, IParticipantList, [
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
    grok.name('session-list')
    grok.require('cmf.ModifyPortalContent')

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


class PendingSessionListingView(grok.View):
    grok.context(IConference)
    grok.template('listing')
    grok.name('pending-session-list')
    grok.require('cmf.ModifyPortalContent')

    title = u'Pending Sessions'

    def provider(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog({
            'portal_type': 'collective.conference.session',
            'path': {
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 2
            },
            'review_state': 'pending'
        })
        objs = [ i.getObject() for i in brains ]
        return TableListingProvider(self.request, ISessionList, objs)
