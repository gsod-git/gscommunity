# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Gscommunity",
			"color": "pink",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": _("Gscommunity")
		},
		{
			"module_name": "Events",
			"color": "pink",
			"icon": "octicon octicon-calendar",
			"type": "module",
			"label": _("Events")
		}
	]
