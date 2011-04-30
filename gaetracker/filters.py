# encoding=utf-8

import hashlib
import logging
import os

from google.appengine.ext import webapp

import markdown as md

register = webapp.template.create_template_register()


@register.filter
def markdown(text):
    return md.markdown(text)


@register.filter
def gravatar(author, size=48):
    email = author and author.email() or 'info@example.com'
    return 'http://www.gravatar.com/avatar/%s?s=%s' % (hashlib.md5(email).hexdigest(), size)


@register.filter
def format_label(label, path):
    link = path + '?action=list&amp;label=' + label
    prefix = ''
    if '-' in label:
        prefix, label = label.split('-', 1)
        prefix += ': '
    return u'%s<a href="%s">%s</a>' % (prefix, link, label)


@register.filter
def extra_column(issue, b):
    prefix = b + '-'
    for label in issue.labels:
        if label.startswith(prefix):
            v = label[len(prefix):]
            path = os.environ['PATH_INFO']
            return u'<a href="%s?action=list&amp;label=%s">%s</a>' % (path, label, v)
    return ''
