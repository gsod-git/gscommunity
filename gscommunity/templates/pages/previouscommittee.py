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
	context.title='Previous Committee'
	now=getdate(nowdate())
	committee=frappe.db.get_all('Committee',fields=['name'], filters={'published':1},order_by='creation')
	for item in committee:
		members=frappe.db.get_all('Team Members', fields=['name','year','member','member_name','designation','from_date','to_date']
			, filters={'parent':item.name},order_by='year desc')
		content=[]
		for m in members:
			m.last_name=frappe.db.get_value('Member',m.member,'last_name')
			m.middle_name=frappe.db.get_value('Member',m.member,'middle_name')
			m.public_access=frappe.db.get_value('Member',m.member,'public_profile')
			if m.public_access:
				m.image=frappe.db.get_value('Member',m.member,'image')
			if m.year:
				if int(now.year)>int(m.year):
					content.append(m)
		item.members=content
	context.committee=committee
	context.year=now.year