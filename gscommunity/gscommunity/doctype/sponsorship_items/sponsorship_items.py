# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate
from datetime import date,datetime

class SponsorshipItems(Document):
	pass
	def autoname(self):
		if self.sponsor_for:
			self.name=self.sponsor_for+' - '+self.item_name.replace('&','and')
		else:
			self.name=self.item_name
	def on_update(self):
		if frappe.db.get_value("DocType", self.sponsorship_type):
			if not self.sponsor_for:
				frappe.throw(frappe._('Please select "Sponsor For" for the selected "Sponsorship Type"'))	

@frappe.whitelist()
def get_items(sponsorship_type):
	now=getdate(nowdate())
	if frappe.db.get_value("DocType", sponsorship_type):
		if sponsorship_type=='Events':
			data=frappe.db.sql('''select name from `tabEvents` where start_date>=%(now)s''',{'now':nowdate()},as_dict=1)
			return data
		elif sponsorship_type=='Samaj Darshan':
			data=frappe.db.get_all('Samaj Darshan',fields=['name','year'],filters={'year':now.year})
			for item in data:
				item.list=frappe.db.get_all('Samaj Darshan Lists',fields=['*'],filters={'parent':item.name,'published':0})
			return data
		else:
			data=frappe.db.get_all(sponsorship_type,fields=['*'])
			return data
@frappe.whitelist()
def get_account_head(docname,doctype):
	if frappe.db.get_value("DocType", doctype):
		if doctype=='Samaj Darshan':
			year=docname.split('-')[1]
			month=docname.split('-')[0]
			parent=doctype+' '+year
			data=frappe.db.get_all(doctype,fields=['accounting_head','accounting_group'],filters={'name':parent})
			return data[0]
		else:
			data=frappe.db.get_all(doctype,fields=['accounting_head','accounting_group'],filters={'name':docname})
			return data[0]
@frappe.whitelist()
def get_yellowpage_feature():
	result=frappe.db.sql('''select * from `tabDocField` where parent="Yellow Pages" and fieldtype="Section Break" order by idx''',as_dict=1)
	return result
@frappe.whitelist(allow_guest=True)
def get_sponsor_feature(type):
	return frappe.db.get_all('Sponsorship Type',fields=['enable_yellowpage'],filters={'name':type})
@frappe.whitelist(allow_guest=True)
def add_yp_feature(section,docname,label,checked):
	features=frappe.get_all('Sponsor YP Feature',fields=['*'],filters={'parent':docname})
	check=0
	enable=0
	if checked=="true":
		enable=1
	elif checked=="false":
		enable=0
	if features:
		for data in features:
			if data.section==section:
				check=1
	if check==0:
		result= frappe.get_doc({
				"doctype": "Sponsor YP Feature","name": nowdate(),"parent": docname,"parentfield": "yp_feature",
				"parenttype": "Sponsorship Items","section": section,"label":label,"enable":enable
				}).insert()
	elif check==1:
		frappe.db.sql('''update `tabSponsor YP Feature` set enable=%(enable)s where section=%(section)s and parent=%(parent)s''',
			{'enable':enable,'section':section,'parent':docname})
@frappe.whitelist()
def get_selected_yp_feature(name):
	result=frappe.db.get_all('Sponsor YP Feature',fields=['*'],filters={'parent':name,'enable':1})
	return result