# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
import frappe.utils
import json
import calendar
from frappe import _
from frappe.utils import getdate
from datetime import date
import frappe.www.list
 
def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	context.show_sidebar=True
	user=frappe.session.user
	member=frappe.db.get_all('Member',fields=['name'],filters={'email':user})
	if member:
		sponsor=frappe.db.get_all('Sponsorship',fields=['*'],filters={'member':member[0].name},order_by='starts_on desc')
		context.sponsor=sponsor
	else:
		sponsor=frappe.db.get_all('Sponsorship',fields=['*'],filters={'email':user},order_by='starts_on desc')
		context.sponsor=sponsor
	context.subscriptions=frappe.db.get_all('Braintree Subscriptions',fields=['*'],filters={'parent':frappe.session.user,'subscription_for':'Sponsorship'})