#!/usr/bin/python2.5
#
# Copyright 2009 Google Inc.
# Licensed under the Apache License, Version 2.0:
# http://www.apache.org/licenses/LICENSE-2.0

"""The module that handles requests for user-facing pages.

This model sets up a base class for requests, and then each
page extends that class to define its own title and other
customizations.
"""

import os

from google.appengine.ext import webapp
from google.appengine.api import users 
from google.appengine.ext import db 
from google.appengine.ext.webapp import template

import models

class BasePage(webapp.RequestHandler):
  """The base class for actual pages to subclass."""

  def get(self):
    self.Render(self.GetTemplateFilename(), self.GetTemplateValues())

  def GetTemplateValues(self, page_title='Welcome'):
    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'

    template_values = {
      'is_admin': users.is_current_user_admin(),
      'url': url,
      'url_linktext': url_linktext,
      'page_title': page_title
      }

    return template_values

  def GetTemplateFilename(self):
    return 'base.html'

  def Render(self, filename, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates', filename)
    self.response.out.write(template.render(path, template_values))


class Home(BasePage):
  """The main page, displays just a message and links to the user."""

  def GetTemplateValues(self):
    template_values = BasePage.GetTemplateValues(self, 'OSSPoints')
    query = db.Query(models.PointsEarner)
    query.order('-points')
    results = query.fetch(limit=10)
    template_values['top_earners'] = results
    return template_values

  def GetTemplateFilename(self):
    return 'home.html'


class PointsForPrizes(BasePage):
  """The signup page, displays a form."""

  def GetTemplateValues(self):
    template_values = BasePage.GetTemplateValues(self, 'Points & Prizes')
    return template_values

  def GetTemplateFilename(self):
    return 'prizes.html'

class AddPoints(BasePage):
  """The signup page, displays a form."""

  def GetTemplateValues(self):
    template_values = BasePage.GetTemplateValues(self, 'Add Points')
    return template_values

  def GetTemplateFilename(self):
    return 'addpoints.html'

class UserPoints(BasePage):
  """The signup page, displays a form."""

  def GetTemplateValues(self):
    username = self.request.get('username')
    if not username:
      username = users.get_current_user().email()
    template_values = BasePage.GetTemplateValues(self, 'User Points')
    query = db.Query(models.PointsEarner)
    query.filter('username =', username)
    points_earner = query.get()
    template_values['username'] = username
    template_values['points_earner'] = points_earner
    return template_values

  def GetTemplateFilename(self):
    return 'userpoints.html'
