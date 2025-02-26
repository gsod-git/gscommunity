# Copyright (c) 2013, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns=[
		("Member") + ":Link/Member:120",
		("Last Name")+":Data:120",
		("First Name")+":Data:120",
		("Spouse Name")+":Data:180",
		("Mailing Type")+":Data:120",
		("Address")+":Data:300"
	]
	data=get_data(filters)
	return columns, data
def get_data(filters):
	data=[]
	conditions=''
	if filters.samaj_darshan:
		conditions+=" and samaj_darshan='%s'"% filters.samaj_darshan
	else:
		conditions+=" and samaj_darshan!=''"
	# Members=frappe.db.sql('''select * from `tabMember` where active=1 {condition} order by last_name,member_name'''.format(condition=conditions),as_dict=1)
	# if Members:
	# 	for member in Members:
	# 		if not member.primary_member_id:
	# 			content=[]
	# 			content.append(member.name)
	# 			content.append(member.last_name)
	# 			content.append(member.member_name)
	# 			spouse=frappe.db.get_all('Other Members',fields=['member_name','last_name'],filters={'relation':'Spouse','parent':member.name})
	# 			spouse_name=''
	# 			if spouse:
	# 				spouse_name=spouse[0].member_name+' '+spouse[0].last_name
	# 			content.append(spouse_name)
	# 			content.append(member.samaj_darshan)
	# 			address=member.address_line_1+','
	# 			if member.address_line_2:
	# 				address = address+member.address_line_2+','
	# 			address = address+member.city+','+member.state+'-'+member.zip_code
	# 			content.append(address)
	# 			data.append(content)
	# return data
	return frappe.db.sql('''select m.name,m.last_name,m.member_name,ifnull(concat_ws(' ',s.member_name,
		s.last_name),''),m.samaj_darshan,concat_ws(', ',m.address_line_1,m.address_line_2,m.city,
		m.state,m.zip_code) from `tabMember` m left join `tabOther Members` s on m.name=s.parent and 
		s.relation="Spouse" where (m.primary_member_id='' or m.primary_member_id is null) 
		{condition} order by m.last_name,m.member_name'''.format(condition=conditions))