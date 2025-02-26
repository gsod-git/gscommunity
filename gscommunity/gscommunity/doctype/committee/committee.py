# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate,nowdate
from datetime import date


class Committee(Document):
	pass
	# def on_update(self):
	# 	if self.table_4:
	# 		for x in self.table_4:
	# 			x.year=x.from_date.year
@frappe.whitelist()
def get_members(name,date):	
	# members = frappe.get_all("Team Members", fields=["member","member_name","designation","from_date","to_date"], filters={"parent":name,"to_date":date})
	condition = ""
	members=frappe.db.sql("""select * from `tabTeam Members` where to_date>= %(date)s and parent=%(name)s""".format(condition), 
				{"date":date,"name":name}, as_dict=1)	
	return members