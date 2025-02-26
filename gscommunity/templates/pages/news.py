# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
# import frappe
# from _future_ import unicode_literals
import frappe
import frappe.utils
import json
from frappe import _


def get_context(context): 
	NewsList=frappe.db.get_all('Community News',fields=['title','date','route','image',],filters={'published':1})
	context.NewsList=NewsList
 

	