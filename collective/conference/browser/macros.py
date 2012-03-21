# Five imports
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize.instance import memoize

from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Products.CMFPlone.browser.interfaces import INavigationTree
from five import grok
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName

from Products.CMFPlone.browser.navtree import NavtreeQueryBuilder
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from DateTime import DateTime

class NavTree(object):
    grok.implements(INavigationTree)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def navigationTreeRootPath(self):
        return '/'.join(self.context.getPhysicalPath())

    def navigationTree(self):
        context = aq_inner(self.context)

        queryBuilder = NavtreeQueryBuilder(context)
        query = queryBuilder()

        strategy = getMultiAdapter((context, self), INavtreeStrategy)

        return buildFolderTree(context, obj=context, query=query, strategy=strategy)

class Macros(BrowserView):

    template = ViewPageTemplateFile('templates/macros.pt')

    @property
    def macros(self):
        return self.template.macros

    def content_tabs(self):
        context = aq_inner(self.context)
        navtree_view = NavTree(context, self.request)
        return [{
            'id':t['id'],
            'name':t['Title'],
            'url':t['getURL'],
            'description':t['Description']
        } for t in navtree_view.navigationTree()['children']]


    def text_to_html(self, text):
        text = text or ''
        pt = getToolByName(self.context, 'portal_transforms')
        return pt.convertTo('text/html', text, mimetype='text/plain').getData()

    def timedelta(self, start, end):
        if isinstance(start, DateTime):
            start=start.asdatetime()
        if isinstance(end, DateTime):
            end=end.asdatetime()
        return start-end

    def person_inline_css(self, person):

        result = """
             min-height:100px;
            text-align:center;
            word-wrap:break-word;
            border-bottom:3px #%s solid;
        """ % getattr(person, 'color', 'cccccc')[:6]

        return result
