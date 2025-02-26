# Copyright (c) 2013, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns = get_columns()
	data = get_participant(filters)
	return columns, data
def get_columns():
	return [
		("Event") + ":Data:120",
		("Competition") + ":Data:120",
		("Choreographer") + ":Data:200",
		("Team Name") + ":Data:120",
		("Participant Name") + ":Data:200",
		("Prize Type") + ":Data:120",
	]
def get_participant(filters):
	condition=get_condition(filters)
	content=[]
	even=filters.events
	team_condition=''
	if filters.competition:
		team_condition+=" and competition='%s'"% filters.competition
	Team=frappe.db.sql('''select * from `tabTeam` where events=%(events)s{condition}'''.format(condition=team_condition),{'events':filters.events},as_dict=1)	
	data=[]	
	for item in Team:
		choreographer=frappe.db.get_all('Event Managing Team',fields=['member_name','member'],filters={'parent':item.name,'member_type':'Choreographer'})[0]
		participant=frappe.db.sql('''select * from `tabEvent Participating Members` where parent=%(parent)s {condition}'''.format(condition=condition),{'parent':item.name},as_dict=1)
		if participant:
			for member in participant:
				content=[]
				content.append(item.events)
				content.append(item.competition)
				content.append(choreographer.member_name+' '+frappe.get_value('Member',choreographer.member,'last_name'))
				content.append(item.song_title)
				content.append(member.member_name+' '+frappe.get_value('Member',member.member,'last_name'))
				content.append(member.prize_type)
				data.append(content)
	return data
def get_condition(filters):
	condition=''	
	if filters.prize_type:
		condition+=" and prize_type='%s'"% filters.prize_type
	return condition