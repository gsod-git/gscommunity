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
	PagesList=frappe.db.get_all('Pages',fields=['name1','published','route','description','image','page_type'], filters={'published':1,'page_type':'Gsy Articles' } )
	context.PagesList=PagesList
	EventsList=frappe.db.sql('''select * from `tabEvents` where published=1 
		and start_date>%(now)s and event_type=%(event_type)s order by start_date'''.format()
		,{'now':getdate(nowdate()),'event_type':'GSY Events'},as_dict=1)	
	for item in EventsList:
		item.dates=getdate(item.start_date).strftime("%d") 
		item.months = frappe.utils.formatdate(item.start_date, "MMM YYYY")
		item.days = calendar.day_name[item.start_date.weekday()] 
	context.GSSEventsList=EventsList 