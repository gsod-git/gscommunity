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
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	else:
		member=frappe.db.get_value('User',frappe.session.user,'username')
		if not frappe.db.get_value('Member',member):
			frappe.throw(_("You need to be a member of GSOD to access this page"), frappe.PermissionError)
	context.title='Elections' 
	elections=frappe.db.sql('''select * from `tabElections` where registration_start_date<=%(now)s and registration_end_date>=%(now)s''',{'now':getdate(nowdate())},as_dict=1)
	context.election=elections	