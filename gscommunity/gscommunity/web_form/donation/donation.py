from __future__ import unicode_literals

import frappe
from frappe.utils import nowdate
import datetime
from datetime import date, datetime, time

def get_context(context):
	# do your magic here
	pass

@frappe.whitelist(allow_guest=True)
def get_account_head(category):
	result=frappe.db.get_all('Donation Category',fields=['accounting_head'],filters={'name':category})
	return result[0]