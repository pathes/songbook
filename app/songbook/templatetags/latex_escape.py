# -*- coding: utf-8 -*-
""" Escape string for generating LaTeX content.

    Usage:
    {{ malicious|latex_escape }}

    Remember: when generating LaTeX content, you should always check
    whether \write18 is disabled!
"""

from django import template
from functools import reduce

register = template.Library()

@register.filter
def latex_escape(x):
    repls = {
        '#': '\# ',
        '$': '\$ ',
        '%': '\% ',
        '&': '\\ampersand ',
        '_': '\_ ',
        '{': '\{ ',
        '}': '\} ',
        '~': '\\textasciitilde ',
        '^': '\\textasciicircum ',
        '\\': '\\textbackslash ',
        '<': '\\textless ',
        '>': '\\textgreater ',
        '♯': '$\sharp$ ',
        '♭': '$\\flat$ ',
    }
    return reduce(
        lambda a, kv: a.replace(*kv), iter(list(repls.items())), str(x)
    )
