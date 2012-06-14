"""
Core functionality for interacting with the HNSearch API.
"""

import requests as req
import simplejson as json

from . import thriftdb
from .date import Date


class News(object):

    def __init__(self):
        self.url = "http://api.thriftdb.com/api.hnsearch.com/items/_search"

    def get(self, **params):
        """Perform a GET request."""
        params = thriftdb.convert(params)
        data = req.get(self.url, params=params)
        self.request = data
        results = json.loads(data.content)
        url = "http://news.ycombinator.com/item?id={0}"
        for result in results['results']:
            result['item']['hn_url'] = url.format(result['item']['id'])
            if result['item'].get('discussion', None) is not None:
                result['item']['discussion']['hn_url'] = url.format(
                    result['item']['discussion']['id'])
        return results

    def date(self, day):
        """Query a specific date."""
        day = Date(day)

    def hours(self, day, start, end):
        """Query a day by specific hours."""
        date = Date(day)
        start = date.hour(start)
        end = date.hour(end)

    def facet(self, term, **params):
        """Facets are almost like searching what can be searched."""
        params['facet'] = term
        return self.get(**params)

    def filter(self, condition, **params):
        """Filter the results to a specific condition."""
        params['filter'] = condition
        return self.get(**params)

    def search(self, term, **params):
        """Perform a search against the HNSearch API."""
        params['q'] = term
        return self.get(**params)
