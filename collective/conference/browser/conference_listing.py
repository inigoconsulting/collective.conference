from five import grok

from Products.ATContentTypes.interfaces.topic import IATTopic
from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.CMFCore.interfaces import ISiteRoot

grok.templatedir('templates')

class TopicConferenceListingView(grok.View):
    grok.context(IATTopic)
    grok.template('conference_listing')
    grok.name('conference_listing')

class FolderConferenceListingView(grok.View):
    grok.context(IATFolder)
    grok.template('conference_listing')
    grok.name('conference_listing')

class SiteRootConferenceListingView(grok.View):
    grok.context(ISiteRoot)
    grok.template('conference_listing')
    grok.name('conference_listing')
