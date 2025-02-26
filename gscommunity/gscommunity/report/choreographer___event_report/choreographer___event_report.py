# Copyright (c) 2013, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns = get_columns()
	data = get_members(filters)
	return columns, data
def get_columns():
	return [
		("Event") + ":Data:120",
		("Competition") + ":Data:120",
		("Choreographer") + ":Data:120",
		("Co Choreographer") + ":Data:120",
		("Manager") + ":Data:120",
		("Team Name") + ":Data:120",
		("Age Group") + ":Data:120",
		("Active Participants") + ":Data:80",
		("InActive Participants") + ":Data:80",
		("Song") + ":Data:80",
		("Song Background") + ":Data:180"		
	]
def get_members(filters):
	condition=get_condition(filters)
	
	Team=frappe.db.sql("""select * from `tabTeam` {condition}""".format(condition=condition),as_dict=1)
	
	data=[]	
	for item in Team:
		content=[]
		choreographer=''
		co_choregrapher=''
		manager=''
		managing_team=frappe.db.get_all('Event Managing Team',fields=['member_name','member_type','member'],filters={'parent':item.name})		
		active_participants=frappe.db.get_all('Event Participating Members',fields=['name'],filters={'parent':item.name,'active':'Active'})
		inactive_participants=frappe.db.get_all('Event Participating Members',fields=['name'],filters={'parent':item.name,'active':'In Active'})
		for team in managing_team:
			member_name=team.member_name+' '+frappe.get_value('Member',team.member,'last_name')
			if team.member_type=="Choreographer":
				choreographer=member_name
			elif team.member_type=="Co-Choreographer":
				co_choregrapher=member_name
			else:
				manager=member_name
		content.append(item.events)
		content.append(item.competition)
		content.append(choreographer)
		content.append(co_choregrapher)
		content.append(manager)
		content.append(item.song_title)
		content.append(item.age_group)
		content.append(len(active_participants))
		content.append(len(inactive_participants))
		if item.song:
			content.append('Yes')
		else:
			content.append('No')
		fullbackground=''
		song_background=frappe.db.get_all('Song Background',fields=['color','from_time','to_time','color_code'],filters={'parent':item.name},order_by='idx')
		for background in song_background:		
			color=''
			if background.from_time:
				color+=background.from_time
			if background.to_time:
				color+='-'+background.to_time		
			if background.color:
				color+='-'+background.color			
			elif background.color_code:
				color+='-'+background.color_code
			color+=';'
			fullbackground+=color
		content.append(fullbackground)		
		data.append(content)
	return data

def get_condition(filters):
	condition=""
	if filters.events:
		condition+=" where events='%s'"% filters.events
		if filters.competition:
			condition+=" and competition='%s'"% filters.competition
	else:
		if filters.competition:
			condition+=" where competition='%s'"% filters.competition	
	condition+=' order by creation desc'
	return condition