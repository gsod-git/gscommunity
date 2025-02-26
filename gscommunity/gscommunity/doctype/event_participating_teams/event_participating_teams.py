# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate,datetime
from datetime import date
from frappe.desk.reportview import get_match_cond, get_filters_cond

class EventParticipatingTeams(Document):
	pass
	def validate(self):		
		validate_competition_settings(self)		

	def on_update(self):
		tableLength=len(self.get("table_7"))	
		# validate_competition_settings(self)	
		if not tableLength:
			tableLength=0
		Members=frappe.db.get_list('Event Participating Members',fields=['member','parent'])
		for x in self.table_7:
			for y in Members:
				if(x.member==y.member and y.parent!=self.name):
					frappe.throw(frappe._("{0} is already in another team. Please select another member").format(x.member))
		Teams=frappe.db.get_all('Participating Teams'
						,fields=['name','team','age_group','performance_duration','no_of_participants']
						,filters={"parent":self.competition,'team':self.name})
		song_duration=0
		if self.song_duration:
			song_duration=self.song_duration
		if self.status=="Approved":
			if not Teams:
				insert_participants(self.name,self.competition,self.song_title,self.age_group,song_duration,tableLength)
			else:
				result=frappe.db.sql("""update `tabParticipating Teams` set team_name=%(team_name)s,
							age_group=%(age_group)s,performance_duration=%(performance_duration)s,
							no_of_participants=%(no_of_participants)s where name=%(name)s"""
							.format(),{
							"name":x.name,
							"team_name":self.song_title,
							"age_group":self.age_group,
							"performance_duration":song_duration,
							"no_of_participants":tableLength
							})

@frappe.whitelist()
def get_upcoming_events(doctype, txt, searchfield,filters, start=0, page_len=50):
	now = datetime.datetime.now()
	return frappe.db.sql("""select name from `tabEvents`
			where start_date > %(date)s			
			""".format(
				match_cond=get_match_cond(doctype),
				start=start,
				page_len=page_len), {					
					"date": now
				})

@frappe.whitelist()
def get_members(doctype, txt, searchfield,filters, start=0, page_len=50):
	ParticipatingMembers=frappe.db.sql("""select member from `tabEvent Participating Members`""")
	MembersList=frappe.db.sql("""select name from `tabMember`""")
	content=[]
	for x in MembersList:
		for y in ParticipatingMembers:
			if y!=x:
				content.append(x)
	return content
@frappe.whitelist()
def get_hall_color(doctype, txt, searchfield,filters, start=0, page_len=50):
	Colors=frappe.db.sql("""select name from `tabColors`""")
	EventHall=frappe.db.get_all('Events',fields=['event_venue'],filters={"name":txt})
	if EventHall:
		for x in EventHall:
			Hall=frappe.db.get_all('Event Halls',fields=['name','any_color'],filters={"name":x.event_venue})
			if not Hall[0].any_color:
				Colors=frappe.db.sql("""select color from `tabHall Colors` where parent=%(name)s"""
					.format(),{"name":Hall[0].name})
	return Colors

@frappe.whitelist()
def insert_participants(name,parent,team,age_group,performance_duration,no_of_participants,teamhead):
	result=frappe.db.sql("""insert into `tabParticipating Teams`
				(name,parent,parentfield,parenttype,team,team_name,age_group,performance_duration,no_of_participants,team_head) 
				values(%(name)s,%(parent)s,%(parentfield)s,%(parenttype)s,%(team)s,%(team_name)s,%(age_group)s,%(performance_duration)s,%(no_of_participants)s,%(teamhead)s) """
   					.format(),{
   					"name":get_random(),
   					"parent":parent,
   					"parentfield":"table_11",
   					"parenttype":"Competition",
   					"team":name,
   					"team_name":team,
   					"age_group":age_group,
   					"performance_duration":performance_duration,
   					"no_of_participants":no_of_participants,
   					"teamhead":teamhead
   					})
	return result

@frappe.whitelist()
def get_random():
	import random 
	import string
	random = ''.join([random.choice(string.ascii_letters
            + string.digits) for n in range(12)])
	Name=frappe.db.get_all('Participating Teams',fields=['name','parent'])
	for x in Name:
		if x.name==random:
			random=get_random()
	return random

@frappe.whitelist()
def validate_competition_settings(self):
	tableLength=len(self.get("table_7"))
	if not tableLength:
		tableLength=0
	settings = frappe.db.get_all("Competition"
			,fields=['maximum_participants','minimum_participants','team_head','max_team_head','performance_duration'],
			filters={'name':self.competition})	
	if(tableLength<settings[0].minimum_participants):
		frappe.msgprint(frappe._("Minimum of {0} participants are required ").format(settings[0].minimum_participants))		
	if(tableLength>settings[0].maximum_participants):
		frappe.throw(frappe._("Maximum of {0} participants are required ").format(settings[0].maximum_participants))	
	team_head=''
	for m in self.table_11:		
		if m.member_type==settings[0].team_head:
			team_head=m.member			
	teamHead=frappe.db.get_all('Event Managing Team',fields=['member','member_type','parent'],
			filters={'member':team_head})	
	checkVal=0
	for x in teamHead:
		if x.parent == self.name:
			checkVal=1
	if checkVal==0:
		if len(teamHead)>=settings[0].max_team_head:
			frappe.throw(frappe._("Maximum of {0} teams can be handled by a single {1}")
				.format(settings[0].max_team_head,settings[0].team_head))
	validate_managing_teams(self)
	validate_active_members(self)

@frappe.whitelist()
def validate_managing_teams(self):
	data=[]	
	for x in self.table_11:
		if data:
			for m in data:
				if(m!=x.member_type):
					data.append(x.member_type)
		else:
			data.append(x.member_type)
	for d in data:
		count=0
		for x in self.table_11:
			if(x.member_type==d):
				count=count+1
				if(count>1):
					frappe.throw(frappe._("Only one {0} can be added").format(x.member_type))
@frappe.whitelist()
def validate_active_members(self):
	for x in self.table_11:
		if not x.active:
			frappe.throw(frappe._("test"))
	for x in self.table_7:
		if not x.active:
			frappe.throw(frappe._("test"))