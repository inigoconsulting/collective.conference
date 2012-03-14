from plone.indexer.decorator import indexer
from collective.conference.conference import IConference
from collective.conference.session import ISession

@indexer(IConference)
def c_conference_rooms(obj, **kw):
    return obj.rooms

@indexer(ISession)
def s_conference_rooms(obj, **kw):
    return obj.conference_rooms
