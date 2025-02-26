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
	now=getdate(nowdate())
	SponsorshipTypeList=frappe.db.get_all('Sponsorship Items', fields=['name','sponsorship_type','item_amount','ribbon_image','image','validity','item_name','display_id']
		,filters={'sponsorship_type':'Advertising Plans'} ,order_by = "display_id")
	for data in SponsorshipTypeList:
		data.Sponsors=frappe.db.get_all('Sponsorship',fields=['name','sponsor_name','email','phone','expires_on'],filters={'sponsorship_plan':data.name,'published':1})
		for item in data.Sponsors:
			if item.expires_on:
				if item.expires_on>=now:
					yp=frappe.db.get_all('Yellow Pages',fields=['name','route'],filters={'user':item.email})
					if yp:
						item.yp=yp[0].route
				else:
					frappe.db.set_value("Sponsorship", item.name , "published", 0)
			else:
				yp=frappe.db.get_all('Yellow Pages',fields=['name','route'],filters={'user':item.email})
	context.SponsorshipTypeList=SponsorshipTypeList