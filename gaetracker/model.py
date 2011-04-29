# encoding=utf-8

from google.appengine.ext import db

class Model(db.Model):
    pass


class TrackerIssue(Model):
    id = db.IntegerProperty()
    date_created = db.DateTimeProperty(auto_now_add=True)
    date_updated = db.DateTimeProperty(auto_now_add=True)

    author = db.UserProperty()
    owner = db.UserProperty()

    summary = db.StringProperty()
    description = db.TextProperty()
    labels = db.StringListProperty()

    comment_count = db.IntegerProperty(default=0)

    def status(self):
        for label in self.labels:
            if label.lower().startswith('status-'):
                return label[7:]
        return 'New'


class TrackerIssueComment(Model):
    issue_id = db.IntegerProperty(required=True)
    date_created = db.DateTimeProperty(auto_now_add=True)
    author = db.UserProperty()
    text = db.TextProperty()
