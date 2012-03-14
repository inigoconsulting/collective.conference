from five import grok
from collective.conference.conference import IConference

grok.templatedir('templates')

class AttendanceView(grok.View):
    grok.context(IConference)
    grok.template('attendance_list')
    grok.name('attendance')


