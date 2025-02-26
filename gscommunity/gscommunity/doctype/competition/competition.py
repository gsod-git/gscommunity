# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Competition(Document):
	pass
	def autoname(self):		
		self.name = self.events+'-'+self.competition_type
	def validate(self):
		if self.event_start_date:
			if(self.registration_start_date>=self.event_start_date or self.registration_end_date>=self.event_start_date):
				frappe.throw(frappe._('Registration start date and end date should be before the start of event.'))
			if(self.registration_start_date>self.registration_end_date):
				frappe.throw(frappe._('Registration end date should be after the start date'))
		if self.performance_duration:
			if self.performance_duration.find(':')==-1:
				frappe.throw(frappe._('Performance Duration should be in the format MM:SS'))