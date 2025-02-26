# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
# import frappe
# from _future_ import unicode_literals
import frappe
import frappe.utils
import json
from frappe import _
from frappe.auth import LoginManager

def get_context(context):
	doc = frappe.get_doc("Contact Us", "Contact Us")
	name=doc.name
	context.list= frappe.db.get_all('Contact Info',fields=['title','contact_person','email_id'],filters={'parent':doc.name},order_by="idx asc")
	context.web=doc.website_address
	context.feedback=doc.feedback_email_id
	