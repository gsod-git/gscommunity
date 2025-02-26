from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import getdate,datetime
from datetime import date

def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	else:
		member=frappe.db.get_all('Member',fields=['name'],filters={'email':frappe.session.user})
		if not member:
			frappe.throw(_("You need to be a member of GSOD to access this page"), frappe.PermissionError)	
	