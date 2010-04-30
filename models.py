#!/usr/bin/python2.5
#
# Copyright 2009 Google Inc.
# Licensed under the Apache License, Version 2.0:
# http://www.apache.org/licenses/LICENSE-2.0

"""A module for the datastore model classes.

This module contains datastore model classes
for petition signers and clusters, as well
as constants for memcache key prefixes.
"""

from google.appengine.ext import db

class PointsEarner(db.Model):
  """Stores information about the votes in a given region.

  Attributes:
    username: Username, includes domain.
    points: Total number of points
    firsttime: Whether they got first time bonus.
  """
  username = db.StringProperty()
  points = db.IntegerProperty(default=0)
  firsttime = db.BooleanProperty(default=False)

class PointsLogEntry(db.Model):
  earner = db.ReferenceProperty(PointsEarner, collection_name='logs')
  reason = db.StringProperty(default='No reason given')
  points = db.IntegerProperty()
  date = db.DateTimeProperty(auto_now_add=True)
