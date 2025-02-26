# Copyright (c) 2013, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt
from frappe.utils import getdate,datetime
from datetime import date

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()
	data = get_memberlist(filters)
	return columns, data

def get_columns():
	return [
		_("Member ID") + ":Data:140",
		_("Member Name") + ":Data:200",
		_("Status") + "Data:70",
		# _("Date of Birth")+ ":Date:100",
		_("Membership Type") + ":Link/Membership Type:180", 
		_("Membership Amount") + ":Data:120",
		_("Membership Expiry Date") + ":Date:120",
		# _("Gender") + "::60", 
		# _("Company") + ":Link/Company:120"
	]

def get_memberlist(filters):
	conditions = get_conditions(filters)
	Member=frappe.db.get_all('Membership Type',fields=['name'],filters={'name':filters.membership_type})
	data=[]
	content=[]
	now=datetime.date.today()
	for team in Member:
		Active=0
		if filters.active == "Active":
			Active=1
		if filters.active == "Inactive":
			Active=0
		members=frappe.db.sql("""select * from `tabMember` where membership_type=%(name)s and active=%(active)s""".format(conditions),{"name":team.name,"active":Active},as_dict=1)
		if members:
			for member in members:
				content.append(member.name)
				content.append(member.member_name)
				if member.active == 1:
					content.append("Active")
				if member.active == 0:
					content.append("Inactive")
				content.append(member.membership_type)
				content.append(member.membership_expiry_date)
				content.append(member.membership_amount)
                data.append(content)
	return data

def get_conditions(filters):
	conditions = ""
	if filters.get("year"):
		year=filters["year"]
		conditions += " year(membership_expiry_date) = '%s'" % year

	return conditions