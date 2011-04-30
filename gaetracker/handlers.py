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
                if v:
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
        issue.labels = [ 'Status-New' ]
        user = users.get_current_user()
        if user is not None:
            issue.author = user
            issue.owner = user
        return issue


class EditAction(SubmitAction):
    template = 'edit.tpl'

    def get_issue(self):
        issue_id = int(self.rh.request.get('id'))
        issue = model.TrackerIssue.gql('WHERE id = :1', issue_id).get()
        if issue is None:
            raise Exception('Issue %u does not exist.' % issue_id)
        return issue


class ViewAction(Action):
    template = 'view.tpl'

    def get(self):
        issue_id = int(self.rh.request.get('id'))
        issue = model.TrackerIssue.gql('WHERE id = :1', issue_id).get()
        issue.labels = sorted(issue.labels, key=lambda l: ('-' not in l, l.lower()))
        self.render({
            'issue': issue,
            'comments': model.TrackerIssueComment.gql('WHERE issue_id = :1 ORDER BY date_created', issue_id).fetch(100),
            'user': users.get_current_user(),
            'path': self.rh.request.path,
        })


class CommentAction(Action):
    def post(self):
        issue_id = int(self.rh.request.get('id', '0'))
        if not issue_id:
            raise Exception('Issue id not specified.')

        issue = model.TrackerIssue.gql('WHERE id = :1', issue_id).get()
        if issue is None:
            raise Exception('Issue %u does not exist.' % issue_id)

        comment = model.TrackerIssueComment(issue_id=issue_id)
        author = users.get_current_user()
        if author is not None:
            comment.author = author
        comment.text = self.rh.request.get('text')
        comment.put()

        self.rh.redirect(self.rh.request.path + '?action=view&id=' + str(issue_id))


class ListAction(Action):
    template = 'list.tpl'

    def get(self):
        label = self.rh.request.get('label')
        if label:
            issues = model.TrackerIssue.gql('WHERE labels = :1 ORDER BY date_created DESC', label).fetch(1000)
        else:
            issues = model.TrackerIssue.all().order('-date_created').fetch(1000)
        self.render({
            'issues': issues,
            'path': self.rh.request.path,
            'filter': label,
        })


class Tracker(webapp.RequestHandler):
    handlers = {
        'comment': CommentAction,
        'edit': EditAction,
        'list': ListAction,
        'submit': SubmitAction,
        'view': ViewAction,
    }

    def get(self):
        self.call('get')

    def post(self):
        self.call('post')

    def call(self, method):
        action = self.request.get('action', 'list')
        if action in self.handlers:
            getattr(self.handlers[action](self), method)()
        else:
            self.reply('Don\'t know how to handle action "%s".' % action)

    def render(self, template_name, data, content_type='text/html'):
        logging.debug(u'Data for %s: %s' % (template_name, data))
        filename = os.path.join(os.path.dirname(__file__), 'templates', template_name)
        self.reply(template.render(filename, data), content_type=content_type)

    def reply(self, content, content_type='text/plain', status=200):
        self.response.headers['Content-Type'] = content_type + '; charset=utf-8'
        self.response.out.write(content)

handlers = [
    ('.*', Tracker),
]
