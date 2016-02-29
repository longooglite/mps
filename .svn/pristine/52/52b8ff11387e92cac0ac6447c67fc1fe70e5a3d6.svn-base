# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import os.path
import tornado.template

#   Ability to load tornado templates from multiple directories.

class MPSTemplateLoader(tornado.template.BaseLoader):
	def __init__(self, **kwargs):
		super(MPSTemplateLoader, self).__init__(**kwargs)
		self.directoryList = []

	def addDirectory(self, _absolutePath):
		self.directoryList.append(_absolutePath)

	def resolve_path(self, name, parent_path=None):
		return name

	def _create_template(self, name):
		if name.startswith('/'):
			return self._makeTemplate(name, name)

		for dir in self.directoryList:
			path = os.path.join(dir, name)
			if os.path.exists(path):
				return self._makeTemplate(path, name)

		return tornado.template.Template("Template %s not found" % name, name=name, loader=self)

	def _makeTemplate(self, _path, _name):
		with open(_path, "rb") as f:
			template = tornado.template.Template(f.read(), name=_name, loader=self)
			return template

