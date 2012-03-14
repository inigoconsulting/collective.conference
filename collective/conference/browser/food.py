from five import grok
from collective.conference.conference import IConference

grok.templatedir('templates')

class ParticipantView(grok.View):
    grok.context(IConference)
    grok.template('food')
    grok.name('food')


