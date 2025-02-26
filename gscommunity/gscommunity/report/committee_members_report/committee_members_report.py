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
	data = get_members(filters)

	return columns, data
def get_columns():
	return [
		_("Member") + ":Link/Member:120",
		_("Member Name") + ":Data:200",
		_("Designation") + "::180", 
		_("From Date") + ":Date:120",
		_("To Date") + ":Date:120"
	]

def get_members(filters):	
	Committee=frappe.db.get_all('Committee',fields=['name','title'],filters={'title':filters.committee})
	data=[]	
	now=datetime.date.today()
	for team in Committee:
		members=frappe.db.sql("""select * from `tabTeam Members` where parent=%(name)s and year=%(year)s""", 
				{"name":team.name,"year":filters.year}, as_dict=1)
		if members:
			for member in members:
				content=[]
				content.append(member.member)
				content.append(member.member_name+' '+frappe.get_value('Member',member.member,'last_name'))
				content.append(member.designation)
				content.append(member.from_date)
				content.append(member.to_date)
				data.append(content)
	return data

@frappe.whitelist()
def get_years():
	year_list = frappe.db.sql_list('''select distinct year from `tabTeam Members` where year!="None" ORDER BY year DESC''')
	if not year_list:
		year_list = [getdate().year]
	return "\n".join(str(year) for year in year_list)