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
	return [
		("Member") + ":Link/Member:120",
		("Full Name") + ":Data:120",
		("Membership Type") + ":Data:120",
		("Status") + ":Data:100",		
		("Email") + ":Data:120",
		("Mobile Number") + ":Data:80",
		("Address") + ":Data:200",
		("Payment Date") + ":Data:200"
	]
def get_data(filters):
	data=[]
	now=getdate(nowdate())
	condition=''
	email_list=""
	if filters.emails:	
		email=filters.emails.split(',')
		i=1
		email_len=len(email)
		for item in email:
			if i<email_len:
				email_list=email_list+'"'+item+'",'				
			else:
				email_list=email_list+'"'+item+'"'	
			i=i+1
		condition='where email in ('+email_list+')'
	setting=frappe.get_single('General Settings')
	members=frappe.db.sql('''select * from `tabMember` {condition}'''.format(condition=condition),as_dict=1)
	if members:
		for mem in members:
			content=[]
			membership=frappe.db.sql('''select name from `tabMembership` where 
				(member=%(member)s or member=%(primary_member)s) and to_date>=%(now)s''',
				{'member':mem.name,'now':now,'primary_member':mem.primary_member_id},as_dict=1)
			if membership:
				payment=frappe.db.get_all('Payment Entries',filters={'ref_id':membership[0].name,'payment_date':('<=',filters.get('payment_date'))},
					fields=['payment_date','name'])
				if payment:			
					content.append(mem.name)
					full_name=mem.member_name+' '+mem.last_name
					content.append(full_name)
					content.append(mem.membership_type)
					if mem.active:
						content.append('Active')
					else:
						content.append('In Active')
					content.append(mem.email)
					content.append(mem.phone_no)
					address=mem.address_line_1+','
					if mem.address_line_2:
						address = address+mem.address_line_2+','
					address = address+mem.city+','+mem.state+'-'+mem.zip_code
					content.append(address)
					content.append(payment[0].payment_date)
					data.append(content)				
	return data