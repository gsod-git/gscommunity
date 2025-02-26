# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
import frappe.utils
import json
from frappe import _
import frappe.www.list
 
def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	context.show_sidebar=True
	user=frappe.session.user
	user_name=frappe.get_value('User',user,'username')
	member=frappe.get_doc('Member',user_name)
	bookings=frappe.db.get_all('Bookings',fields=['*'],filters={'member':user_name})
	if not bookings:
		bookings=frappe.db.get_all('Bookings',fields=['*'],filters={'email':user})
	context.booking=bookings
	context.user=user_data