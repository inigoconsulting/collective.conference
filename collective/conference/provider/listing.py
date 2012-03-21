from zope import schema
from zope.interface import Interface, alsoProvides
from zope.schema.interfaces import IField
from z3c.table.table import SequenceTable
from z3c.table.column import Column
from z3c.table.interfaces import IColumn
from zope import component as zca
from five import grok
from zope.globalrequest import getRequest
from plone.autoform.interfaces import OMITTED_KEY

class SchemaTable(SequenceTable):

    def __init__(self, context, request, schema, cssClasses={}):
        super(SchemaTable, self).__init__(context, request)
        self.schema = schema
        self.cssClasses = cssClasses

    def setUpColumns(self):
        cols = [IndexColumn(self.context, self.request, self)]
        omitted_fields = list([
            i[1] for i in self.schema.queryTaggedValue(OMITTED_KEY, []) if i[2]
        ])
        for name, field in schema.getFieldsInOrder(self.schema):
            if name in omitted_fields:
                continue
            column = zca.getMultiAdapter(
                (self.context, self.request, self, field),
                IColumn
            )
            cols.append(column)
        return cols

class IndexColumn(Column):
    grok.provides(IColumn)

    header = '#'

    def renderCell(self, item):
        return '%03d' % (self.table.values.index(item) + 1)

class FieldColumn(grok.MultiAdapter, Column):
    grok.provides(IColumn)
    grok.adapts(None, None, SchemaTable, IField)

    def __init__(self, context, request, table, field):
        self.field = field
        super(FieldColumn, self).__init__(context, request, table)

    @property
    def header(self):
        return self.field.title

    def renderCell(self, item):
        obj = self.table.schema(item, item)
        result = self.field.query(obj, u'')
        if result is None:
            return u''
        if self.field.__name__ == 'title':
            return '<a href="%s">%s</a>' % (item.absolute_url(), result)
        return result

class TableListingProvider(object):

    def __init__(self, request, schema, objs):
        self.request = request
        self.schema = schema
        self.objs = objs

    def render(self):
        table = SchemaTable(self.objs, self.request, self.schema, 
            { 'table': 'table table-condensed table-striped'}
        )
        table.startBatchingAt = 1000 # disable batching for now
        table.update()
        return table.render()
