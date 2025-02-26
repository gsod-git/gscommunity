# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils import getdate,datetime,nowdate
from datetime import date

class Elections(WebsiteGenerator):
	pass
	def on_update(self):		
		self.route=self.title.lower().replace(' ','-').replace('&','and')
	def get_context(self,context):
		now=getdate(nowdate())
		election=frappe.db.get_all('Elections',fields=['*'],filters={'name':self.name})
		if election:			
			if election[0].registration_start_date<=now and election[0].registration_end_date>=now:
				context.election=election[0]
			else:
				frappe.db.set_value('Elections',self.name,'published',0)
				frappe.throw(frappe._('The page you are looking for is not found.'))
@frappe.whitelist()
def get_member_nomination(member,election):
	nomination=frappe.db.get_all('Election Nominations',filters={'election':election,'member':member})
	if nomination:
		return '1'
	else:
		return '0'