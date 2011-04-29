# encoding=utf-8

import hashlib
import logging

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
