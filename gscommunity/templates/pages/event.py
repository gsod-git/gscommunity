# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
# import frappe
# from _future_ import unicode_literals
import frappe
import frappe.utils
import json
import calendar
from frappe import _
from frappe.utils import getdate,nowdate
from datetime import date
 
def get_context(context):	
	EventsList=get_events('GSOD Events')
	GSSEventsList=get_events('GSS Events')
	GSYEventsList=get_events('GSY Events')   
	context.GSYEventsList=GSYEventsList
	context.GSSEventsList=GSSEventsList
	context.EventsList=EventsList 
	context.Advetisment=context.AdsMaxImpressionCount 

@frappe.whitelist()
def get_events(event_type):
	now=getdate(nowdate())
	EventsList=frappe.db.sql('''select * from `tabEvents` where published=1 
		and (start_date>%(now)s or end_date>=%(now)s) and event_type=%(event_type)s order by start_date'''.format()
		,{'now':now,'event_type':event_type},as_dict=1)	
	for item in EventsList:
		item.dates=getdate(item.start_date).strftime("%d") 
		if item.banner_image:
			item.image= frappe.db.get_all('File',fields=['thumb_file_1','thumb_file_2','file_url'],filters={'file_url':item.banner_image,'attached_to_doctype':'Events'})
		item.months = frappe.utils.formatdate(item.start_date, "MMM YYYY")
		item.days = calendar.day_name[item.start_date.weekday()]		
		if item.venue_type=='Event Hall':
			if item.event_venue:
				venue_detail=frappe.db.get_all('Event Halls'
						,fields=['name','address_line_1','address_line_2','city','state','zip_code'],
						filters={'name':item.event_venue})[0]
				item.location=venue_detail.address_line_1
				item.address_line_2=venue_detail.address_line_2
				item.city=venue_detail.city
				item.state=venue_detail.state
				item.zip_code=venue_detail.zip_code    
	return EventsList