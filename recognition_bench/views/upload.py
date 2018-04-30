from pyramid.response import Response
from pyramid.view import (
	view_defaults,
	view_config
)

import os
import boto3

@view_defaults(route_name='upload', renderer='templates/upload.jinja2')
class Upload(object):
	def __init__(self, request):
		self.request = request

	@view_config(request_method='GET')
	def get(self):
		return {}