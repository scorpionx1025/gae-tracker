# encoding=utf-8

import logging
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import model


class Action:
    def __init__(self, rh):
        self.rh = rh

    def render(self, data):
        self.rh.render(self.template, data)


class SubmitAction(Action):
    template = 'submit.tpl'

    def get(self):
        self.render({
            'issue': self.get_issue(),
            'path': self.rh.request.path,
        })

    def post(self):
        issue = self.get_issue()

        for k in self.rh.request.arguments():
            v = self.rh.request.get(k)
            if k == 'f.labels':
                issue.labels = [l.strip() for l in v.split(',') if l.strip()]
            elif k == 'f.owner':
                issue.owner = users.User(v)
            elif k.startswith('f.'):
                setattr(issue, k[2:], v)

        last = model.TrackerIssue.all().order('-id').get()
        if last is None:
            issue.id = 1
        else:
            issue.id = last.id + 1

        issue.put()

        self.rh.redirect(self.rh.request.path + '?action=view&id=' + str(issue.id))

    def get_issue(self):
        issue = model.TrackerIssue()
        issue.author = users.get_current_user()
        return issue


class EditAction(SubmitAction):
    template = 'edit.tpl'

    def get_issue(self):
        return model.TrackerIssue.gql('WHERE id = :1', int(self.rh.request.get('id'))).get()


class ViewAction(Action):
    template = 'view.tpl'

    def get(self):
        self.render({
            'issue': model.TrackerIssue.gql('WHERE id = :1', int(self.rh.request.get('id'))).get(),
        })


class Tracker(webapp.RequestHandler):
    handlers = {
        'edit': EditAction,
        'submit': SubmitAction,
        'view': ViewAction,
    }

    def get(self):
        self.call('get')

    def post(self):
        self.call('post')

    def call(self, method):
        action = self.request.get('action')
        if action in self.handlers:
            getattr(self.handlers[action](self), method)()
        else:
            self.reply('Don\'t know how to handle action "%s".' % action)
        

    def render(self, template_name, data, content_type='text/html'):
        logging.debug(data)
        filename = os.path.join(os.path.dirname(__file__), 'templates', template_name)
        self.reply(template.render(filename, data), content_type=content_type)

    def reply(self, content, content_type='text/plain', status=200):
        self.response.headers['Content-Type'] = content_type + '; charset=utf-8'
        self.response.out.write(content)

handlers = [
    ('.*', Tracker),
]
