# encoding=utf-8

import logging
import os

from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import issues
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
        })

    def post(self):
        data = dict([(x, self.rh.request.get(x)) for x in self.rh.request.arguments()])
        if 'labels' in data:
            data['labels'] = [l.strip() for l in data['labels'].split(',') if l.strip()]
        issue = issues.update(data)
        self.rh.redirect(self.rh.request.path + '?action=view&id=' + str(issue.id))

    def get_issue(self):
        issue = model.TrackerIssue()
        issue.labels = [ 'Open' ]
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
        })


class CommentAction(Action):
    def post(self):
        issue_id = int(self.rh.request.get('id', '0'))
        issues.add_comment(issue_id, users.get_current_user(), self.rh.request.get('text'))
        self.rh.redirect(self.rh.request.path + '?action=view&id=' + str(issue_id))


class ListAction(Action):
    template = 'list.tpl'

    def get(self):
        label = self.rh.request.get('label')
        issues_ = issues.find_issues(label, closed=self.rh.request.get('closed'))

        self.render({
            'issues': issues_,
            'filter': label,
            'columns': self.get_columns(issues_),
        })

    def get_columns(self, issues):
        columns = []
        for issue in issues:
            for label in issue.labels:
                if '-' in label:
                    k, v = label.split('-', 1)
                    if k not in columns:
                        columns.append(k)
        return sorted(columns)


class ExportAction(Action):
    def get(self):
        data = issues.export_json(self.rh.request.get('label') or None)
        self.rh.reply(data)


class ImportAction(Action):
    template = 'import.tpl'

    def get(self):
        self.render({ })

    def post(self):
        data = simplejson.loads(self.rh.request.get('dump'))
        issues.import_all(data)
        self.rh.redirect(self.rh.request.path)


class ImportOneAction(Action):
    def post(self):
        issues.update(simplejson.loads(self.rh.request.get('data')))


class Tracker(webapp.RequestHandler):
    handlers = {
        'comment': CommentAction,
        'edit': EditAction,
        'export': ExportAction,
        'import': ImportAction,
        'import-one': ImportOneAction,
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
        data['path'] = self.request.path
        data['user'] = users.get_current_user()
        # logging.debug(u'Data for %s: %s' % (template_name, data))
        filename = os.path.join(os.path.dirname(__file__), 'templates', template_name)
        self.reply(template.render(filename, data), content_type=content_type)

    def reply(self, content, content_type='text/plain', status=200):
        self.response.headers['Content-Type'] = content_type + '; charset=utf-8'
        self.response.out.write(content)

handlers = [
    ('.*', Tracker),
]
