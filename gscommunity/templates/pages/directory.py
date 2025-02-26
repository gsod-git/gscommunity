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
from frappe.utils import getdate
from datetime import date
 
def get_context(context):
	if frappe.session.user == 'Guest':
		frappe.throw(frappe._('You are not permitted to access this page.'), frappe.PermissionError)
	member = frappe.request.cookies.get('member_id')
	if not member or member == "":
		frappe.throw(frappe._('You are not permitted to access this page.'), frappe.PermissionError)
	MemberList=frappe.db.get_all('Member', fields=['*'],filters={"active":1})
	context.MemberList=MemberList 