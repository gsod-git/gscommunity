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
		("Competition") + ":Data:120",		
		("Choreographer") + ":Data:120",
		("Co Choreographer") + ":Data:120",
		("Manager") + ":Data:120",
		("Team Name") + ":Data:120",
		("Age Group") + ":Data:120",
		("Participants") + ":Data:300",
		("Song Background") + ":Data:180"		
	]

def get_data(filters):
	data=[]
	condition=''
	if filters.competition:
		condition=" and name='%s'"% filters.competition
	competition=frappe.db.sql('''select * from `tabCompetition` where events=%(events)s {condition}'''.format(condition=condition),{'events':filters.events},as_dict=1)
	if competition:
		for comp in competition:
			teams=frappe.db.get_all('Participating Teams',fields=['*'],filters={'parent':comp.name})
			
			if teams:
				for team in teams:
					content=[]
					content.append(team.parent)	
					managing_team=frappe.db.get_all('Event Managing Team',fields=['*'],filters={'parent':team.team})
					manager=''
					co_choreographer=''
					choreographer=''
					for m_team in managing_team:
						member_name=m_team.member_name+' '+frappe.get_value('Member',m_team.member,'last_name')
						if m_team.member_type=='Choreographer':
							choreographer=member_name
						elif m_team.member_type=='Co-Choreographer':
							co_choreographer=member_name
						else:
							manager=member_name
					content.append(choreographer)
					content.append(co_choreographer)
					content.append(manager)
					content.append(team.team_name)
					content.append(team.age_group)
					participants=frappe.db.get_all('Event Participating Members',fields=['*'],filters={'parent':team.team})
					participant_list=''
					for participant in participants:
						part_details=frappe.get_doc('Member',participant.member)
						participant_list=participant_list+participant.member_name
						if part_details.last_name:
							participant_list+=' '+part_details.last_name
						participant_list+=','
					content.append(participant_list)
					song_background=frappe.db.get_all('Song Background',fields=['color','from_time','to_time','color_code'],filters={'parent':team.team},order_by='idx')
					fullbackground=''
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