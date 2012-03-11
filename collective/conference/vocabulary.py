from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from five import grok
from zope.schema.interfaces import IVocabularyFactory
from incf.countryutils import data as countrydata

class TShirtSize(object):

    def __call__(self, context):
        return SimpleVocabulary.fromValues(
            ['S', 'M', 'L', 'XL', 'XXL', 'XXXL']
        )

grok.global_utility(TShirtSize, IVocabularyFactory,
        name="collective.conference.vocabulary.tshirtsize")

class Countries(object):

    def __call__(self, context):
        return SimpleVocabulary.fromValues(sorted([
            i.decode('utf-8') for i,c in countrydata.cn_to_ccn.items() if c != '248'
        ]))

grok.global_utility(Countries, IVocabularyFactory,
        name="collective.conference.vocabulary.countries")


class SessionTypes(object):

    def __call__(self, context):
        return SimpleVocabulary.fromValues([
            u'Talk',
            u'Hackfest',
            u'Workshop',
            u'Discussion'
        ])

grok.global_utility(SessionTypes, IVocabularyFactory,
        name="collective.conference.vocabulary.sessiontype")

class SessionLevels(object):

    def __call__(self, context):
        return SimpleVocabulary.fromValues([
            u'Beginner',
            u'Intermediate',
            u'Advanced'
        ])

grok.global_utility(SessionLevels, IVocabularyFactory,
        name="collective.conference.vocabulary.sessionlevel")




