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

class IRegistrationForm(IParticipant):
    form.widget(captcha=CaptchaFieldWidget)
    captcha = schema.TextLine(title=u"",
                            required=False)

@form.validator(field=IRegistrationForm['captcha'])
def validateCaptca(value):
    site = getSite()
    request = getRequest()
    captcha = CaptchaValidator(site, request, None,
            IRegistrationForm['captcha'], None)
    captcha.validate(value)


class RegistrationForm(form.SchemaAddForm):
    grok.name('register')
    grok.context(IConference)
    schema = IRegistrationForm
    label = u"Register a session"

    def create(self, data):
        obj = Participant()
        inc = getattr(self.context, 'registrant_increment', 0) + 1
        data['id'] = 'participant-%s' % inc
        self.context.registrant_increment = inc
        item = createContentInContainer(
            self.context,
            "collective.conference.participant", 
            **data
        )
        return obj

    def add(self, obj):
        pass
