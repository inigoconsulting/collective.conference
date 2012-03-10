from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from five import grok
from zope.schema.interfaces import IVocabularyFactory

class TShirtSize(object):

    def __call__(self, context):
        return SimpleVocabulary.fromValues(
            ['S', 'M', 'L', 'XL', 'XXL', 'XXXL']
        )

grok.global_utility(TShirtSize, IVocabularyFactory,
        name="collective.conference.vocabulary.tshirtsize")
