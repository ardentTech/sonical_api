from django_filters.filters import BooleanFilter
from django_filters.widgets import BooleanWidget


class SonicalBooleanFilter(BooleanFilter):

    def __init__(self, *args, **kwargs):
        super(SonicalBooleanFilter, self).__init__(widget=BooleanWidget)
