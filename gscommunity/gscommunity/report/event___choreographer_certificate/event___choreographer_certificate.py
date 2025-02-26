# Copyright (c) 2013, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns=[
		("Member") + ":Link/Member:120",
		("Choreographer / Co-Choreographer")+":Data:250",
		("Teams")+":Data:300"
	]
	data=get_data(filters)
	return columns, data
def get_data(filters):
	data=[]
	members=frappe.db.sql('''select distinct mt.member from `tabEvent Managing Team` mt left join 
		`tabTeam` t on t.name=mt.parent where t.events=%(events)s and t.status="Approved" and mt.member_type != "Manager"''',
		{'events':filters.events},as_dict=1)
	if members:
		for member in members:
			member_info=frappe.db.get_all('Member',fields=['*'],filters={'name':member.member})[0]
			content=[]
			content.append(member.member)
			member_name=member_info.member_name
			if member_info.middle_name:
				member_name=member_name+' '+member_info.middle_name
			member_name=member_name+' '+member_info.last_name
			content.append(member_name)
			teams=frappe.db.sql('''select distinct song_title from `tabTeam` t inner join `tabEvent Managing Team` et on et.parent=t.name
				where t.events=%(events)s and et.member=%(member)s and et.member_type!="Manager"''',{'events':filters.events,'member':member.member},as_dict=1)
			if teams:
				team_names=''
				for item in teams:
					team_names+=item.song_title+','
				content.append(team_names)
			data.append(content)
	return data