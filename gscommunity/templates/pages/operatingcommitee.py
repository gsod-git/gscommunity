# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
import frappe.utils
import json
import calendar
from frappe import _
from frappe.utils import getdate,nowdate
from datetime import date
 
def get_context(context):
	now=getdate(nowdate())
	context.title='Operating Committee' 
	committee=frappe.db.get_all('Committee',fields=['name'], filters={'published':1},order_by='creation')
	for item in committee:
		item.members=frappe.db.get_all('Team Members', fields=['name','year','member','member_name','designation','from_date','to_date']
			, filters={'parent':item.name,'year':now.year},order_by='year desc')
		for member in item.members:
			member.last_name=frappe.db.get_value('Member',member.member,'last_name')
			member.middle_name=frappe.db.get_value('Member',member.member,'middle_name')
			member.public_access=frappe.db.get_value('Member',member.member,'public_profile')
			if member.public_access:
				member.image=frappe.db.get_value('Member',member.member,'image')
	context.committee=committee	