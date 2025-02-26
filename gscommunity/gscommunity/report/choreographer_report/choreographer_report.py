# Copyright (c) 2013, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_members(filters)
	return columns, data
def get_columns():
	return [
		_("Member") + ":Link/Member:120",
		_("Member Name") + ":Data:200",
		_("Mobile No") + ":Data:100", 
		_("Whatsapp No") + ":Data:100", 
		_("Email") + ":Data:200",
		_("Membership Type") + ":Data:200",
		_("Membership Status") + ":Data:120",
		_("Address Line 1") + ":Data:200",
		_("Address Line 2") + ":Data:200",
		_("City") + ":Data:160",
		_("State") + ":Data:60",
		_("Zip Code") + ":Data:60",		
	]

def get_members(filters):	
	Members=frappe.db.get_all('Member',fields=['*'],order_by='name')
	data=[]	
	for member in Members:
		if not member.email:
			member.email=member.name+'@gsod.org'		
		role=frappe.db.get_all('Has Role',fields=['parent','role'],filters={'parent':member.email,'role':'Choreographer'})
		if role:
			content=[]
			content.append(member.name)
			name=member.member_name
			if member.middle_name:
				name+=' '+member.middle_name
			name+=' '+member.last_name
			content.append(name)
			content.append(member.phone_no)
			content.append(member.mobile_no)
			content.append(member.email)
			content.append(member.membership_type)
			if member.active:
				content.append('Active')
			else:
				content.append('In Active')
			content.append(member.address_line_1)
			content.append(member.address_line_2)
			content.append(member.city)
			content.append(member.state)
			content.append(member.zip_code)
			data.append(content)
	return data