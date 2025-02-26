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
	PrintEventsList=frappe.db.get_all('Events',fields=['name','start_date','end_date','route','location','event_type','start_date'], filters={'published':1}, order_by='start_date')
	EventsList=frappe.db.get_all('Events',fields=['name','start_date','end_date','route','event_type'], filters={'published':1})
	array = [];
	color_code=[]
	color_code.append({'event_name':'GSOD Events','color':'#3700b3'}) 
	color_code.append({'event_name':'GSS Events','color':'#e50041'})
	color_code.append({'event_name':'GSY Events','color':'#edcd1f'})	
	for x in EventsList:
		startdate = x.start_date.strftime("%Y-%m-%d") 
		if(x.event_type == "GSS Events") :
			bgcolor = "#e50041"
		elif(x.event_type == "GSY Events"):
			bgcolor = "#edcd1f"
		else :
			bgcolor = "#3700b3"
		array.append({"title":x.name,"start":startdate,"url":x.route,"color":bgcolor})
	content=[]
	now=getdate(nowdate())
	for x in PrintEventsList:
		if x.start_date>now:
			content.append(x)
	# context.test=content
	context.EventsList=json.dumps(array)
	context.PrintEventsList=content
	context.color_code=color_code