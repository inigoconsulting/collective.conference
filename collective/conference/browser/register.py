from five import grok
from collective.conference.participant import IParticipant, Participant
from collective.conference.conference import IConference
from plone.formwidget.captcha import CaptchaFieldWidget
from plone.formwidget.captcha.validator import CaptchaValidator
from plone.dexterity.utils import createContentInContainer
from plone.directives import form
from zope.component.hooks import getSite
from zope.globalrequest import getRequest
from zope import schema
from z3c.form.error import ErrorViewSnippet

from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.utils import getToolByName


class IRegistrationForm(IParticipant):

    publishinfo = schema.Bool(
        title=u"Show me in attendee list",
        description=u"Check this if you wish your name and contact info" +
                    " to be published in our attendee listing",
        required=False
    )

    form.widget(captcha=CaptchaFieldWidget)
    captcha = schema.TextLine(title=u"",
                            required=False)

@form.validator(field=IRegistrationForm['captcha'])
def validateCaptca(value):
    site = getSite()
    request = getRequest()
    if request.getURL().endswith('kss_z3cform_inline_validation'):
        return

    captcha = CaptchaValidator(site, request, None,
            IRegistrationForm['captcha'], None)
    captcha.validate(value)


class RegistrationForm(form.SchemaAddForm):
    grok.name('register')
    grok.context(IConference)
    grok.require("zope.Public")
    schema = IRegistrationForm
    label = u"Register for this event"


    def create(self, data):
        inc = getattr(self.context, 'registrant_increment', 0) + 1
        data['id'] = 'participant-%s' % inc
        self.context.registrant_increment = inc
        obj = _createObjectByType("collective.conference.participant", 
                self.context, data['id'])

        publishinfo = data['publishinfo']
        del data['captcha']
        del data['publishinfo']
        for k, v in data.items():
            setattr(obj, k, v)

        portal_workflow = getToolByName(self.context, 'portal_workflow')
        if publishinfo:
            portal_workflow.doActionFor(obj, 'anon_publish')
        else:
            portal_workflow.doActionFor(obj, 'anon_hide')
        obj.reindexObject()
        return obj

    def add(self, obj):
        pass
