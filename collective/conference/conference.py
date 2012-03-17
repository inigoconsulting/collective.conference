from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field
from plone.i18n.normalizer.interfaces import IURLNormalizer

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from collective.conference import MessageFactory as _
from plone.dexterity.utils import createContentInContainer

from zope.component import getUtility
from zope.component.hooks import getSite
from Acquisition import aq_parent
from collective import dexteritytextindexer
from collective.dexteritytextindexer.behavior import IDexterityTextIndexer
# Interface class; used to define content-type schema.

class IConference(form.Schema, IImageScaleTraversable):
    """
    A conference event
    """

    logo_image = NamedBlobImage(title=u'Logo')

    form.widget(rooms='plone.z3cform.textlines.TextLinesFieldWidget')
    rooms = schema.List(
        title=u'Available Rooms',
        value_type=schema.TextLine()
    )

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Conference(dexterity.Container):
    grok.implements(IConference)
    grok.provides(IConference)
    
    # Add your class methods and properties here

    def getConference(self):
        site = getSite()
        parent = self
        while parent != site:
            if IConference.providedBy(parent):
                return parent
            parent = aq_parent(parent)
        return None

