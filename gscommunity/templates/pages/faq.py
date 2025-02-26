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
	faq=frappe.db.get_all('FAQ',fields=['name','question','answer'],filters={'publish':1})
	context.faq=faq
	context.title='FAQ'