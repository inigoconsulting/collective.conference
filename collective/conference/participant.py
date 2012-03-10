from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from collective.conference import MessageFactory as _


# Interface class; used to define content-type schema.

class IParticipant(form.Schema, IImageScaleTraversable):
    """
    Conference Participant
    """
    
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/participant.xml to define the content type
    # and add directives here as necessary.
    title = schema.TextLine(title=u"Full name",
            required=True)
    email = schema.TextLine(
        title=u"Email address",
        required=True,
    )
    phone = schema.TextLine(
        title=u"Phone number",
        required=False
    )

    description = schema.Text(
        title=u"Short Bio",
        description=(u"Where you're from, where you work " +
                    "/ study, brief self-description"),
        required=True
    )
    is_vegetarian = schema.Bool(
        title=u"Vegetarian?",
        required=False
    )
    tshirt_size = schema.Choice(
        title=u"T-shirt size",
        vocabulary="collective.conference.vocabulary.tshirtsize",
        required=False
    )
    publishinfo = schema.Bool(
        title=u"Show me in attendee list",
        description=u"Check this if you wish your name and contact info" +
                    " to be published in our attendee listing",
        required=False
    )
    


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Participant(dexterity.Item):
    grok.implements(IParticipant)
    
    # Add your class methods and properties here
