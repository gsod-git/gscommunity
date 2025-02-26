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
	user=frappe.db.get_all('User',fields=['name'],filters={'enabled':1})
	content=[]
	for usr in user:
		roles=frappe.db.get_all('Has Role',fields=['name','role'],filters={'parent':usr.name})
		for role in roles:
			if role.role=='Choreographer':
				content.append(usr)
	for data in content:
		data.member=frappe.db.get_all('Member',fields=['name','member_name','last_name','middle_name','city','state','zip_code','phone_no','image','public_profile']
			,filters={'email':data.name})
	context.user=content