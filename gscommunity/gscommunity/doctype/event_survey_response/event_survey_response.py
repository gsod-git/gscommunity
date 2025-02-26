# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class EventSurveyResponse(Document):	
	def on_update(self):
		for x in self.table_5:
			x.survey = self.event_survey