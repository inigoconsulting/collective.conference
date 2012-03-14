from five import grok
from collective.conference.conference import IConference

grok.templatedir('templates')

class ParticipantView(grok.View):
    grok.context(IConference)
    grok.template('participant_view')
    grok.name('participant')


