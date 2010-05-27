#!/usr/bin/python2.5
#
# Copyright 2009 Google Inc.
# Licensed under the Apache License, Version 2.0:
# http://www.apache.org/licenses/LICENSE-2.0

"""The module that handles requests for services.

This module includes a class for setting up the datastore,
a class for generating cluster JSON, and a class for adding
a petition signer to the datastore.
"""

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import mail

from django.utils import simplejson

import models

class AddPoints(webapp.RequestHandler):
  """Sets up the datastore with a cluster for each state. Use only once."""

  def post(self):
    username = self.request.get('username')
    reason = self.request.get('reason')
    points = int(self.request.get('points'))

    # If no email domain provided, assume @google.com
    if username.find('@') == -1:
      username = username + '@google.com'

    # find points earner, create if doesnt exist
    query = db.Query(models.PointsEarner)
    query.filter('username =', username)
    points_earner = query.get()
    if points_earner is None:
      first_time = True
      points_earner = models.PointsEarner()
      points_earner.username = username
      points_earner.points = points
    else:
      first_time = False
      points_earner.points = points_earner.points + points
    points_earner.put()

    # put in datastore
    points_log_entry = models.PointsLogEntry()
    points_log_entry.earner = points_earner
    points_log_entry.reason = reason
    points_log_entry.points = points
    points_log_entry.put()

    # email username
    sender_email = 'pamelafox@google.com'
    receiver_email = username
    subject = 'Congrats on earning OSSPoints!'
    body = 'You have earned %s points. You now have %s points total.\n' % (points,
                                                                         points_earner.points)

    if first_time:
      body = body + 'Since this is your first time earning OSSPoints, you\'ve also earned the first time bonus (a t-shirt!).\n'

    body = '\nFor more info on earning and redeeming OSSPoints, visit http://osspoints.appspot.com'

    mail.send_mail(sender_email, receiver_email, subject, body)
