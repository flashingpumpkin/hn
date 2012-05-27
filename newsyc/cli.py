"""
Command line goodness.
"""

import sys
from argparse import ArgumentParser
import simplejson as json
from .core import YCombinator

try:
    from pygments import highlight
    from pygments.formatters import Terminal256Formatter as Term256
    from pygments.lexers import JavascriptLexer
    has_pygments = True
except ImportError:
    has_pygments = False


def create_parser():
    """Create the Hacker News command line parser."""
    description = 'A simple and easy-to-use CLI for the HNSearch API.'
    parser = ArgumentParser(prog='hn', description=description)
    parser.add_argument('search', metavar='S', type=str, nargs='*',
                        help="A search term to query for.")
    parser.add_argument('-n', '--limit', metavar='N', type=int,
                        help="Number of results to return. Max 100.")
    parser.add_argument('-s', '--start', metavar='N', type=int,
                        help="Ordinal position of first result.")
    parser.add_argument('-S', '--sort', metavar='S', nargs='*',
                        help="List of pairs to sort results.")
    return parser


def search(options):
    """Perform a search against the HNSearch API."""
    params = {}
    if options.search:
        term = ' '.join(options.search)
        params['q'] = term
    if options.limit:
        params['limit'] = options.limit
    if options.start:
        params['start'] = options.start
    if options.sort:
        sort = options.sort
        if len(sort) == 1:
            sort.append('desc')
        params['sortby'] = ' '.join(sort)
    data = YCombinator().get(**params)
    return decorate(data)


def decorate(stream, indent=2):
    """Turn JSON into something readable."""
    print_formatted_json(sys.stdout, stream, indent)
    sys.stdout.write('\n')


def print_formatted_json(stream, json_data, indentation):
    """Format and print JSON."""
    formatted = json.dumps(json_data, indent=indentation)
    if has_pygments and getattr(stream, 'isatty', lambda: False)():
        formatter = Term256()
        lexer = JavascriptLexer()
        formatted = highlight(formatted, formatter=formatter, lexer=lexer)
    print >> stream, formatted.rstrip()
