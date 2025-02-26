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
	member=frappe.db.get_all('Member',fields=['name'],filters={'email':user})
	content=[]	
	if member:
		managing_team=frappe.db.get_all('Event Managing Team',fields=['*'],filters={'member':member[0].name})
		if managing_team:
			for entry in managing_team:
				Team=frappe.db.get_all('Team',fields=['*'],filters={'name':entry.parent},order_by='creation')				
				if Team:					
					for t in Team:
						content.append(t)
	context.team=content