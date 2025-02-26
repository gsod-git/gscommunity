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
import frappe.www.list
 
def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)

	context.show_sidebar=True
	if frappe.session.user!='Guest' and frappe.session.user=='Administrator':
		context.Userdetails=frappe.db.get_list('User', fields=["username","first_name","full_name","email","last_name","username","gender","mobile_no","birth_date","location"], filters={'username':frappe.session.user})
		context.YellowpagesList=frappe.db.get_all('Yellow Pages', fields=['business_name','route','business_type','category','subcategory','owner_name','email','address','phone','image','description'], filters={'owner':frappe.session.user})
	if frappe.session.user!='Guest' and frappe.session.user!='Administrator':
		context.Userdetails=frappe.db.get_list('User', fields=["first_name","full_name","email","last_name","username","gender","mobile_no","birth_date","location"], filters={'email':frappe.session.user})
		context.YellowpagesList=frappe.db.get_all('Yellow Pages', fields=['business_name','route','business_type','category','subcategory','owner_name','email','address','phone','image','description'], filters={'owner':frappe.session.user})
  
