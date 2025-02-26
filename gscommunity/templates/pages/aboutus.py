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
	doc = frappe.get_doc("About Us Settings", "About Us Settings")
	context.intro=doc.company_introduction	
	