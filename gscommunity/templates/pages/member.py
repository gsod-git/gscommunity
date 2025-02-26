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
	MemberTypeList=frappe.db.get_all('Membership Type', fields=['name','amount','validity','image','membership_info','display_order'],filters={'published':1},order_by='display_order')
	for item in MemberTypeList:
		item.benefits = frappe.db.get_all('Membership Benefits',fields=['title'], filters={'parent':item.name})
	MemberList=frappe.db.get_all('Member', fields=['name','member_name','membership_type','email','gender','last_name','phone_no','date_of_birth','image','address_line_1','city','zip_code'])
	context.MemberTypeList=MemberTypeList
	context.MemberList=MemberList	