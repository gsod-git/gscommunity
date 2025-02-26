# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import today
from frappe.website.utils import clear_cache

class GSODPromotions(Document):
	def autoname(self):		
		self.name = self.advertisement_name

	def on_update(self):
		clear_cache()

	def validate(self):
		if self.published and not self.published_on:
			self.published_on = today()
		if self.sponsor:
			sponsor=frappe.db.get_all('Sponsorship',fields=['name','sponsorship_plan'],filters={'name':self.sponsor})[0]
			plan=frappe.db.get_all('Sponsorship Items',fields=['advertisement_count'],filters={'name':sponsor.sponsorship_plan})
			# if plan[0].advertisement_count==0:
			# 	frappe.throw(frappe._('Advertisement cannot be added for the selected sponsorship'))
			# else:
			# 	ads=frappe.db.get_all('GSOD Promotions',fields=['name','sponsor'],filters={'sponsor':self.sponsor})
			# 	ad=[]
			# 	if ads:
			# 		for data in ads:
			# 			if data.name!=self.name:
			# 				ad.append(data)
			# 	if len(ad)>=plan[0].advertisement_count:
			# 		frappe.throw(frappe._('Only {0} adverisement can be added for the selected sponsorship_type').format(plan[0].advertisement_count))


@frappe.whitelist()
def get_duration(sponsor):
	sponsor=frappe.db.get_all('Sponsorship',fields=['sponsorship_plan','starts_on','expires_on','sponsorship_type'],filters={'name':sponsor})[0]
	plan=frappe.db.get_all('Sponsorship Type',fields=['advertisement_timing'],filters={'name':sponsor.sponsorship_type})
	impression=frappe.get_value('Sponsorship Items',sponsor.sponsorship_plan,'advertisement_count')
	data=[]
	data.append({'advertisement_timing':plan[0].advertisement_timing,'starts_on':sponsor.starts_on,'expires_on':sponsor.expires_on,'impression':impression})
	return data[0]

@frappe.whitelist(allow_guest=True) 
def add_pagecount(name,pagecount,maxviews): 
	remove=0
	if name and frappe.db.exists('GSOD Promotions', name): 
		sno = frappe.get_doc('GSOD Promotions', name) 
		sno.views=sno.views+1;
		if sno.views>=maxviews:
			sno.status='Expired'
			remove=1
		sno.db_update()
	return remove

@frappe.whitelist(allow_guest=True) 
def top_add_pagecount(name,pagecount,maxviews):
	remove=0
	if name and frappe.db.exists('GSOD Promotions', name): 
		sno = frappe.get_doc('GSOD Promotions', name) 		
		sno.views=sno.views+1;
		if sno.views>=maxviews:
			sno.status='Expired'
			remove=1
		sno.db_update()
	return remove

@frappe.whitelist()
def change_status(name,status):
	if frappe.db.get_value("GSOD Promotions", name):	
		frappe.db.set_value("GSOD Promotions", name , "status", status)