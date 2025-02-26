# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class GeneralSettings(Document):
	pass
# @frappe.whitelist()
# def get_types(doctype, txt, searchfield,filters, start=0, page_len=50):
# 	

@frappe.whitelist(allow_guest=True)
def get_validity(membershiptype):
	memtype=frappe.get_doc("General Settings", "General Settings")
	return memtype
@frappe.whitelist(allow_guest=True)
def get_menu_settings(member):
	settings=frappe.get_doc("General Settings", "General Settings")
	yp=frappe.db.get_all('Yellow Pages',fields=['name'],filters={'user':frappe.session.user})
	# user_role=frappe.db.get_all('Has Role',fields=['role'],filters={'parent':frappe.session.user,'role':'Choreographer'})
	volunteer=frappe.db.get_all('Volunteer',fields=['name'],filters={'member':member})
	sponsor=frappe.db.get_all('Sponsorship',fields=['name','sponsorship_type'],filters={'member':member},or_filters={'email':frappe.session.user})
	bookings=frappe.db.get_all('Bookings',fields=['name'],filters={'member':member})
	team=frappe.db.get_all('Event Managing Team',filters={'member':member})
	yp_data=0
	# role=0
	new_sp=0
	booking=0
	if yp:
		yp_data=1
	else:
		if sponsor:
			for item in sponsor:
				s_type=frappe.db.get_value('Sponsorship Type',item.sponsorship_type,'enable_yellowpage')
				if s_type:
					new_sp=1
	# if user_role:
	# 	role=1
	team=1 if team else 0
	volunteer_id=volunteer[0].name if volunteer else ''
	sp=1 if sponsor else 0		
	if bookings:
		booking=1
	else:
		bookings=frappe.db.get_all('Bookings',fields=['name'],filters={'email':frappe.session.user})
		if bookings:
			booking=1
	content=[]
	content.append({'yp':yp_data,'volunteer':volunteer_id,'sp':sp,'new_sp':new_sp,'booking':booking,'team':team})	
	return content[0]
@frappe.whitelist(allow_guest=True)
def get_sponsor_items(doctype, txt, searchfield,filters, start=0, page_len=50):
	result=frappe.db.sql('''select si.name from `tabSponsorship Items` si left join `tabSponsorship Type` st on st.name=si.sponsorship_type where st.enable_yellowpage=1''')
	return result