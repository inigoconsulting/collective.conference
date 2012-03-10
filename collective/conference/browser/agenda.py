from five import grok
from collective.conference.conference import IConference
from collective.conference.room import IRoom
from collective.conference.session import ISession
from Products.CMFCore.utils import getToolByName
import json
from datetime import datetime, timedelta
from Products.AdvancedQuery import Le, Ge, Generic, And, Eq
from zope.security import checkPermission

grok.templatedir('templates')

class AgendaView(grok.View):
    grok.context(IConference)
    grok.name('agenda')
    grok.template('agenda')

    def rooms(self):
        result = []
        catalog = getToolByName(self.context, 'portal_catalog')
        for brain in catalog({
            'portal_type':'collective.conference.room',
            'path': { 'query': '/'.join(self.context.getPhysicalPath()),
                        'depth': 1 }
            }):

            result.append(brain.getObject())
        return result
        
    def days(self):
        result = []
        delta = self.context.endDate-self.context.startDate
        for i in range(delta.days if delta.seconds == 0 else delta.days + 1):
            result.append({
                'id':i,
                'year':self.context.startDate.year,
                'month':self.context.startDate.month,
                'date':self.context.startDate.day + i
            })
        return result

    def script(self):
        initcode = ''

        for day in self.days():
            for room in self.rooms():
                initcode += """
                    $('#calendar-%s-%s').fullCalendar($.extend({
                        events: "%s",
                        year: %s,
                        month: %s,
                        date: %s
                    }, opts))
                """ % (
                    day['id'],
                    room.id, 
                    '%s/events.json' % room.absolute_url(),
                    day['year'],
                    day['month'] - 1,
                    day['date']
                    )

        editable = checkPermission('cmf.ModifyPortalContent', self.context)
        result = """
         $(document).ready(function () {
            var opts = {
               defaultView: 'agendaDay',
               header:'',
               height:1000,
               minTime:8,
               maxTime:18,
               allDaySlot: false,
               editable: %s,
               eventResize: function (event, dayDelta, minuteDelta, revertFunc,
                                        jsEvent, ui, view) {
                        $.post(event.url + '/updateStartEnd',
                              { 'operation': 'resize',
                                'dayDelta': dayDelta,
                                'minuteDelta': minuteDelta})
               },
               eventDrop: function (event, dayDelta, minuteDelta, revertFunc,
                                        jsEvent, ui, view) {
                        $.post(event.url + '/updateStartEnd',
                              { 'operation': 'drag',
                                'dayDelta': dayDelta,
                                'minuteDelta': minuteDelta})
               }
            }

            %s
        });
        """ % ('true' if editable else 'false', initcode)

        return result

class EventJson(grok.View):
    grok.context(IRoom)
    grok.name('events.json')

    def render(self):
        self.request.response.setHeader('Content-Type','text/json')
        start = int(self.request.get('start', 0))
        end = int(self.request.get('end', 0))
        result = []
        for event in self.events(datetime.fromtimestamp(start),
                                datetime.fromtimestamp(end)):
            result.append({
                'id':event.id,
                'title':event.title,
                'start': event.startDate.isoformat(),
                'end':event.endDate.isoformat(),
                'allDay': False,
                'url': event.absolute_url()
            })
        return json.dumps(result)

    def events(self, start, end):
        catalog = getToolByName(self.context, 'portal_catalog')

        queries = [
            Eq('portal_type', 'collective.conference.session'),
            Generic('path',
                {'query': '/'.join(self.context.getPhysicalPath()),
                     'depth': 2}
            ),
            Ge('start', start),
            Le('end', end)
        ]
        result = []
        for brain in catalog.evalAdvancedQuery(And(*queries)):
            result.append(brain.getObject())
        return result


class Update(grok.View):
    grok.context(ISession)
    grok.name('updateStartEnd')

    def render(self):
        self.request.response.setHeader('Content-Type','text/json')
        dayDelta = int(self.request.get('dayDelta', 0))
        minuteDelta = int(self.request.get('minuteDelta', 0))
        operation = self.request.get('operation', '')
        secondsDelta = minuteDelta * 60

        delta = timedelta(dayDelta, secondsDelta)

        if operation == 'resize':
            self.context.endDate = self.context.endDate + delta
        elif operation == 'drag':
            self.context.startDate = self.context.startDate + delta
            self.context.endDate = self.context.endDate + delta
        return ''

