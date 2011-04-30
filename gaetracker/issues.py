# encoding=utf-8

import datetime
import os

from google.appengine.dist import use_library
use_library('django', '0.96')

from django.utils import simplejson
from google.appengine.api import taskqueue
from google.appengine.api import users

import model


def get_issue_by_id(issue_id):
    """Loads or creates an issue."""
    if issue_id:
        issue = model.TrackerIssue.gql('WHERE id = :1', int(issue_id)).get()
        if issue is None:
            issue = model.TrackerIssue(id=int(issue_id))
    else:
        issue = model.TrackerIssue()
        last = model.TrackerIssue.all().order('-id').get()
        if last is None:
            issue.id = 1
        else:
            issue.id = last.id + 1
    return issue


def update(data):
    """Takes a dictionary of strings, parses and updates/creates the issue."""
    issue = get_issue_by_id(data.get('id', None))
    for k, v in data.items():
        if k in('id', 'comment_count'):
            v = int(v)
        if k in ('author', 'owner'):
            v = users.User(v)
        if k in ('date_created', 'date_updated'):
            v = datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
        setattr(issue, k, v)

    if issue.id:
        issue.comment_count = model.TrackerIssueComment.gql('WHERE issue_id = :1', issue.id).count()

    issue.put()
    return issue


def add_comment(issue_id, author, text):
    issue = model.TrackerIssue.gql('WHERE id = :1', int(issue_id)).get()
    if issue is None:
        raise Exception('Issue %s does not exist.', issue_id)

    comment = model.TrackerIssueComment(issue_id=issue_id)
    if author is not None:
        comment.author = author
    comment.text = text
    comment.put()

    issue.date_updated = datetime.datetime.now()
    issue.comment_count = model.TrackerIssueComment.gql('WHERE issue_id = :1', issue.id).count()
    issue.put()


def import_all(data, delayed=True):
    path = os.environ['PATH_INFO']
    for item in data:
        if delayed:
            taskqueue.add(url=path, params={ 'action': 'import-one', 'data': simplejson.dumps(item) })
        else:
            update(item)


def export_json(label=None):
    if label:
        issues = model.TrackerIssue.gql('WHERE labels = :1 ORDER BY date_created DESC', label)
    else:
        issues = model.TrackerIssue.all().order('-date_created')

    data = [{
        'id': i.id,
        'date_created': i.date_created.strftime('%Y-%m-%d %H:%M:%S'),
        'date_updated': i.date_updated.strftime('%Y-%m-%d %H:%M:%S'),
        'author': i.author and i.author.email(),
        'owner': i.owner and i.owner.email(),
        'summary': i.summary,
        'description': i.description,
        'labels': i.labels,
        'comment_count': i.comment_count,
        'comments': [{
            'date_created': c.date_created.strftime('%Y-%m-%d %H:%M:%S'),
            'author': c and c.author.email(),
            'text': c.text,
        } for c in model.TrackerIssueComment.gql('WHERE issue_id = :1', i.id).fetch(1000)],
    } for i in issues.fetch(1000)]

    return simplejson.dumps(data, ensure_ascii=False, indent=True)


def find_issues(label=None, closed=False):
    """Finds issues with the specified label (or all).

    Unless closed is set, hides issues with the Closed label."""
    if label:
        issues = model.TrackerIssue.gql('WHERE labels = :1 ORDER BY date_created DESC', label).fetch(1000)
    else:
        issues = model.TrackerIssue.all().order('-date_created').fetch(1000)
    if not closed:
        issues = [i for i in issues if 'Closed' not in i.labels]
    return issues
