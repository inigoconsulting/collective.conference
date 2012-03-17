from five import grok
from plone.app.layout.viewlets.interfaces import IAboveContent
from zope.interface import Interface

grok.templatedir('templates')

class NavigationViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(IAboveContent)

    grok.template('navigation_viewlet')

    def is_enabled(self):
        getConference = getattr(self.context, 'getConference', None)
        if getConference:
            return True
        return False
