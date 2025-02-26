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
	members=frappe.db.get_all('Team Members', fields=['name','member','member_name','designation','from_date','to_date'],
		order_by='year desc')
	content=[]
	year=[]
	now=getdate(nowdate())
	for m in members:		
		if now.year>m.from_date.year:				
			if not m.from_date.year in year:
				year.append(m.from_date.year)	
	for y in year:
		president=frappe.db.get_all('Team Members', fields=['member_name','member'],
			filters={'year':y,'designation':'President'})
		chairman=frappe.db.get_all('Team Members', fields=['member_name','member'],
			filters={'year':y,'designation':'Chairman'})
		pres=''
		chair=''
		if president:
			p_middle_name=frappe.db.get_value('Member',president[0].member,'middle_name')
			p_last_name=frappe.db.get_value('Member',president[0].member,'last_name')
			pres=president[0].member_name
			if p_middle_name:
				pres=pres+' '+p_middle_name
			pres=pres+' '+p_last_name
		if chairman:
			middle_name=frappe.db.get_value('Member',chairman[0].member,'middle_name')
			last_name=frappe.db.get_value('Member',chairman[0].member,'last_name')
			chair=chairman[0].member_name
			if middle_name:
				chair=chair+' '+middle_name
			chair=chair+' '+last_name
		content.append({'year':y,'president':pres,'chairman':chair})
	context.members=members
	context.committee=content
	context.title='Past Presidents/Chairmen'