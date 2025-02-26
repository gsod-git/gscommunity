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
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	else:
		member=frappe.db.get_all('Member',fields=['name'],filters={'email':frappe.session.user})
		if not member:
			frappe.throw(_("You need to be a member of GSOD to access this page"), frappe.PermissionError)
		else:
			now=getdate(nowdate())
			darshan=frappe.db.get_all('Samaj Darshan',fields=['year','name'],order_by='year desc')
			for data in darshan:
				data.list=frappe.db.get_all('Samaj Darshan Lists',fields=['name','month','published','pdf','parent'],filters={'published':1,'parent':data.name},order_by='idx desc')
			context.darshan=darshan
	context.title='Samaj Darshan Archives'