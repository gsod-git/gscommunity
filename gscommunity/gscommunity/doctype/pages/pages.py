# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import calendar
from frappe.website.website_generator import WebsiteGenerator
from frappe.website.utils import clear_cache
from frappe.utils import getdate
from datetime import date

class Pages(WebsiteGenerator):
	def autoname(self):
		
		self.name = self.name1

	def on_update(self):
		clear_cache()

	def validate(self):
		if not self.route:
			self.route = self.scrub(self.name)
		super(Pages, self).validate()

	def get_context(self,context):   
		
		PagesList=frappe.db.get_all('Pages',fields=['name1','published','route','description','image'], filters={'published':1,'name1':self.name } )
		for item in PagesList:
			item.PagesSections=frappe.db.get_all('Page Sections',fields=['title','description','module_name','no_of_records','block_style','image'], filters={'parent':item.name1 }, order_by='idx asc')
			for data in item.PagesSections: 
				if data.module_name:
					data.Module=frappe.db.get_all(data.module_name,fields=["*"],filters={'published':1},limit_page_length=data.no_of_records)
					for doctype in data.Module:
						doctype.details=frappe.db.get_all('Team Members',fields=['member','member_name','designation'], filters={'parent':doctype.name })
		context.PagesList = PagesList 
