# encoding=utf-8

import datetime
import os

from django.utils import simplejson
from google.appengine.api import taskqueue
from google.appengine.api import users

import model


def import_one(data):
    issue = model.TrackerIssue.gql('WHERE id = :1', data['id']).get()
    if issue is None:
        issue = model.TrackerIssue(id=data['id'])
    for k, v in data.items():
        if k in ('author', 'owner'):
            v = users.User(v)
        if k in ('date_created', 'date_updated'):
            v = datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
        setattr(issue, k, v)
    issue.put()


def import_all(data):
    path = os.environ['PATH_INFO']

    for item in data:
        taskqueue.add(url=path, params={ 'action': 'import-one', 'data': simplejson.dumps(item) })
        # import_one(item)
