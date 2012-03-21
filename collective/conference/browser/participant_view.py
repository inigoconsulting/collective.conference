from five import grok
from collective.conference.participant import IParticipant

grok.templatedir('templates')

class ParticipantView(grok.View):
    grok.context(IParticipant)
    grok.template('participant_view')
    grok.name('view')
    grok.require('zope2.View')
