# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.website.utils import clear_cache
from frappe.utils import getdate,nowdate
from datetime import date

class BusinessListingCategory(WebsiteGenerator):
	def autoname(self): 
		self.name = self.name1 

	def on_update(self):
		clear_cache()

	def validate(self):
		if not self.route:
			self.route = self.scrub(self.name)
		super(BusinessListingCategory, self).validate() 

	def get_context(self,context):
		now=getdate(nowdate())
		SponsorshipTypeList=frappe.db.get_all('Sponsorship Items', fields=['name','ribbon_image'],order_by = "display_id")
		for data in SponsorshipTypeList:
			data.SponsorsBusinessList=frappe.db.get_all('Sponsorship', fields=['sponsor_name','sponsorship_type','sponsorship_plan','expires_on','email','name'], filters={'published': 1,'sponsorship_plan':data.name})
			for item in data.SponsorsBusinessList:
				if item.expires_on:	
					if item.expires_on>=now:
						item.YellowpagesList=frappe.db.get_all('Yellow Pages', fields=['*'], filters={'published': 1,'status':'Approved','sponsor':item.name,'category':self.name},order_by='business_name asc')
					else:
						frappe.db.set_value("Sponsorship", item.name , "published", 0)
				# else:
				# 	item.YellowpagesList=frappe.db.get_all('Yellow Pages', fields=['business_name','route','business_type','category','subcategory','owner_name','email','address','phone','image','description'], filters={'published': 1,'user':item.email,'category':self.name,'status':'Approved'},order_by='business_name asc')
		context.SponsorshipTypeList=SponsorshipTypeList
		YellowpagesList=frappe.db.sql('''select * from `tabYellow Pages` where business_type=%(b_type)s and published=1 and category=%(category)s and status=%(status)s and expires_on>=%(now)s order by business_name asc'''
			,{'b_type':'Member','category':self.name,'status':'Approved','now':now},as_dict=1)
		context.YellowpagesList=YellowpagesList
		yp=frappe.db.get_all('Yellow Pages', fields=['*'], filters={'published': 1,'status':'Approved','sponsor':'SP-00002','category':self.name},order_by='business_name asc')
		context.yp=yp
		context.title=self.name