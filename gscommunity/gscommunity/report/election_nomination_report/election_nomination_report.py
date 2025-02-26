# Copyright (c) 2013, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import getdate,datetime,nowdate
from datetime import date

def execute(filters=None):
	columns, data = [], []
	columns=get_columns(filters)
	data=get_data(filters)
	return columns, data
def get_columns(filters):
	columns=[
		("Member") + ":Link/Member:120",
		("Member Name")+":Data:120",
		("Email")+":Data:150",
		("Mobile Number")+":Data:120",
	]
	election=frappe.db.get_all('Elections',fields=['*'],filters={'name':filters.elections})
	if election:
		if election[0].require_parent_name:
			columns.append(("Parent's Name")+":Data:120")
		columns.append(("First Choice")+":Data:120")
		columns.append(("Second Choice")+":Data:120")
		if election[0].max_choice=='3':
			columns.append(("Third Choice")+":Data:120")
	columns.append(("Membership Status")+":Data:120")
	columns.append(("Address")+":Data:200")
	columns.append(("Payment Date")+":Date:120")
	return columns
def get_data(filters):
	data=[]
	members=frappe.db.get_all('Election Nominations',fields=['*'],filters={'election':filters.elections})
	election=frappe.db.get_all('Elections',fields=['*'],filters={'name':filters.elections})
	setting=frappe.get_single('General Settings')
	now=getdate(nowdate())
	if members:
		for member in members:
			content=[]
			content.append(member.member)
			content.append(member.member_name+' '+frappe.get_value('Member',member.member,'last_name'))
			content.append(member.email)
			content.append(member.mobile_number)
			member_info=frappe.get_doc('Member',member.member)
			if election[0].require_parent_name:
				content.append(member.parent_name+' '+frappe.get_value('Member',member.parent_mem_id,'last_name'))
			election_choices=frappe.db.get_all('Election Nomination Choice',fields=['*'],
				filters={'parent':member.name})
			first_choice=''
			second_choice=''
			third_choice=''
			for choice in election_choices:
				if choice.choice_type=='First Choice':
					first_choice=choice.designation
				elif choice.choice_type=='Second Choice':
					second_choice=choice.designation
				else:
					third_choice=choice.designation
			content.append(first_choice)
			content.append(second_choice)
			if election[0].max_choice=='3':
				content.append(third_choice)
			if member_info.active:
				content.append('Active')
			else:
				content.append('In Active')			
			address=member_info.address_line_1+','
			if member_info.address_line_2:
				address = address+member_info.address_line_2+','
			address = address+member_info.city+','+member_info.state+'-'+member_info.zip_code
			content.append(address)			
			membership=frappe.db.sql('''select name from `tabMembership` where 
				(member=%(member)s or member=%(primary_member)s) and to_date>=%(now)s order by creation desc''',
				{'member':member_info.name,'now':now,'primary_member':member_info.primary_member_id},as_dict=1)
			if membership:
				payment=frappe.db.get_all('Payment Entries',filters={'ref_id':membership[0].name},fields=['payment_date','name'])
				if payment:
					content.append(payment[0].payment_date)
			data.append(content)
	return data