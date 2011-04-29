# encoding=utf-8

from google.appengine.ext import webapp

import markdown as md

register = webapp.template.create_template_register()

@register.filter
def markdown(text):
    return md.markdown(text)
