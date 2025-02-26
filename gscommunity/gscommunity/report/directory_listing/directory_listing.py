# Copyright (c) 2013, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns=get_columns(filters)
	data=get_data(filters)
	return columns, data
def get_columns(filters):
	return [
		("Member") + ":Link/Member:120",
		("Last Name") + ":Data:120",
		("First Name") + ":Data:120",
		("Spouse Name") + ":Data:200",
		("Membership Type") + ":Data:120",
		("Status") + ":Data:100",		
		("Email") + ":Data:120",
		("Mobile Number") + ":Data:80",
		("Address") + ":Data:200",
		("Created By") + ":Data:120"
	]
def get_data(filters):
	data=[]
	condition=get_conditions(filters)
	members=frappe.db.sql('''select * from `tabMember` where self_relation="Self" and primary_member_id is null{condition}'''.format(condition=condition),as_dict=1)
	if members:
		for member in members:
			content=[]
			content.append(member.name)
			content.append(member.last_name)
			content.append(member.member_name)
			spouse=frappe.db.get_all('Other Members',fields=['member_name','last_name'],filters={'relation':'Spouse','parent':member.name})
			spouse_name=''
			if spouse:
				spouse_name=spouse[0].member_name+' '+spouse[0].last_name
			content.append(spouse_name)
			content.append(member.membership_type)
			if member.active:
				content.append('Active')
			else:
				content.append('In Active')
			content.append(member.email)
			content.append(member.phone_no)
			address=member.address_line_1+','
			if member.address_line_2:
				address = address+member.address_line_2+','
			address = address+member.city+','+member.state+'-'+member.zip_code
			content.append(address)
			user=frappe.get_doc('User',member.owner)
			content.append(user.full_name)
			data.append(content)
	return data
def get_conditions(filters):
	condition=''
	if filters.membership_type:
		condition+=" and membership_type='%s'"% filters.membership_type
	condition+=get_active_filters(filters)	
	condition+=' order by last_name,member_name'
	return condition
def get_active_filters(filters):
	condition=''
	if filters.status:
		if filters.status=='Active':
			condition+=' and active=1'
		elif filters.status=='In Active':
			condition+=' and active=0'
	return condition