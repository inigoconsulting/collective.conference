from five import grok

from collective.conference.conference import IConference

grok.templatedir('templates')

class ConferenceView(grok.View):
    grok.context(IConference)
    grok.name('conference_view')
    grok.template('conference_view')
    grok.require('zope2.View')
