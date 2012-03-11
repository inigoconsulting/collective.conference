from five import grok
from collective.conference.conference import IConference

grok.templatedir('templates')

class LocationDetails(grok.View):
    grok.context(IConference)
    grok.template('location')
    grok.name('locationinfo')
