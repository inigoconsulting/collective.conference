from five import grok
from collective.conference.session import ISession, Session
from collective.conference.conference import IConference
from plone.formwidget.captcha import CaptchaFieldWidget
from plone.formwidget.captcha.validator import CaptchaValidator
from plone.dexterity.utils import createContentInContainer
from plone.directives import form
from zope.component.hooks import getSite
from zope.globalrequest import getRequest
from zope import schema
from datetime import timedelta

class IProposalForm(ISession):
    form.widget(captcha=CaptchaFieldWidget)
    captcha = schema.TextLine(title=u"",
                            required=False)
    form.omitted('conference_rooms')

@form.validator(field=IProposalForm['captcha'])
def validateCaptca(value):
    site = getSite()
    request = getRequest()

    if request.getURL().endswith('kss_z3cform_inline_validation'):
        return

    captcha = CaptchaValidator(site, request, None,
            IProposalForm['captcha'], None)
    captcha.validate(value)


class ProposalForm(form.SchemaAddForm):
    grok.name('propose')
    grok.context(IConference)
    grok.require("zope.Public")
    schema = IProposalForm
    label = u"Propose a session"

    def create(self, data):
        obj = Session()
        inc = getattr(self.context, 'session_increment', 0) + 1
        data['id'] = 'session-%s' % inc
        data['startDate'] = self.context.startDate
        data['endDate'] = self.context.startDate + timedelta(0, 3600)
        self.context.session_increment = inc
        item = createContentInContainer(
            self.context,
            "collective.conference.session", 
            **data
        )
        return obj

    def add(self, obj):
        pass
