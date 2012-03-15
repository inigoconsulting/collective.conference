from five import grok
from collective.conference.conference import IConference

grok.templatedir('templates')

class ParticipantListView(grok.View):
    grok.context(IConference)
    grok.template('participant_list')
    grok.name('participant_list')

