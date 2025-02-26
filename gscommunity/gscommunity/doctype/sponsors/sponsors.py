# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils import getdate, add_months, add_to_date
from frappe.website.utils import clear_cache
from frappe.utils import getdate
from datetime import date

class Sponsors(WebsiteGenerator):
	def autoname(self):
		
		self.name = self.sponsor_name

	def on_update(self):
		clear_cache()

	def validate(self):
		if not self.route:
			self.route = self.scrub(self.name)
		super(Sponsors, self).validate()

	def get_context(self,context): 
		SponsorsList=frappe.db.get_all('Sponsors', fields=['name','route','company_name','logo','sponsorship_type','starts_on','expires_on','website_url','phone','email','address','description'], filters={'name':self.name})
		context.SponsorsList=SponsorsList 
		context.title=self.name

@frappe.whitelist(allow_guest=True)
def add_months(date, months):
	return add_to_date(date, months=int(months))
