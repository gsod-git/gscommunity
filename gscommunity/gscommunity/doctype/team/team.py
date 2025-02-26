# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate,datetime,nowdate,today
from datetime import date
from frappe.desk.reportview import get_match_cond, get_filters_cond

class Team(Document):	
	def validate(self):
		# if self.flag=='yes':
		team_head=''
		team_head_id=''			
		settings = frappe.db.get_all("Competition",fields=['team_head'],filters={'name':self.competition})	
		for x in self.table_11:
			if x.member_type==settings[0].team_head:
				team_head=x.member_name
				team_head_id=x.member
		checkrole=check_role(self,team_head_id)
		validate_competition_settings(self)			
		validate_managing_teams(self)
		validate_active_members(self)
		validate_trophy(self)
		validate_age_group(self)
		validate_song_background(self)		
		tableLength=len(self.get("table_7"))	
		if not tableLength:
			tableLength=0
		AllTeams=frappe.db.get_all('Team',fields=['name'],filters={'competition':self.competition})		
		for data in AllTeams:
			item=frappe.db.get_list('Event Participating Members',fields=['member','parent'],filters={'parent':data.name})
			for x in self.table_7:
				for y in item:
					if x.member==y.member and y.parent!=self.name:
						team=frappe.db.get_all('Team',fields=['song_title'],filters={'name':y.parent})
						choreo=frappe.db.get_all('Event Managing Team',fields=['member','member_name'],filters={'parent':y.parent,'member_type':'Choreographer'})
						if choreo:
							frappe.throw(frappe._("{0} is already in another team {1} and {2} is the choreographer for that team. Please select another member").format(x.member_name,team[0].song_title,choreo[0].member_name))
						else:
							frappe.throw(frappe._("{0} is already in another team {1}. Please select another member").format(x.member_name,team[0].song_title))
		Teams=frappe.db.get_all('Participating Teams'
						,fields=['name','team','age_group','performance_duration','no_of_participants']
						,filters={"parent":self.competition,'team':self.name})
		song_duration=0
		if self.song_duration:
			song_duration=self.song_duration
		if checkrole==1 and self.flag=='' and self.status=='Waiting for approval':
			self.status="Approved"		
		if self.status=="Approved":
			assign_role(team_head_id,checkrole)
		if self.status=='Finalized' and self.flag=='':
			if not Teams:
				insert_participants(self.name,self.competition,self.song_title,self.age_group,song_duration,tableLength,team_head)
			else:
				result=frappe.db.sql("""update `tabParticipating Teams` set team_name=%(team_name)s,
							age_group=%(age_group)s,performance_duration=%(performance_duration)s,
							no_of_participants=%(no_of_participants)s,team_head=%(team_head)s where name=%(name)s"""
							.format(),{
							"name":x.name,"team_name":self.song_title,"age_group":self.age_group,
							"performance_duration":song_duration,"no_of_participants":tableLength,
							"team_head":team_head
							})
		self.flag=''
		if self.status=='Waiting for approval' or self.status=="Approved":			
			frappe.msgprint(frappe._('Your team is successfully registered. Admin will review your team and will contact you soon.'))		

	def on_trash(self):
		if self.status=='Finalized':
			roles=frappe.db.get_all('Team Edit Role',fields=['*'])
			check=0
			if roles:
				for role in roles:
					u_role=	frappe.db.get_all('Has Role',fields=['role'],filters={'parent':frappe.session.user,'role':role.role})
					if u_role:
						check=1					
			if check==0:
				frappe.throw(frappe._('You do not have permission to delete a finalized team {0}').format(self.name))
			else:
				team=frappe.db.get_all('Participating Teams',fields=['name'],filters={'team':self.name,'parent':self.competition})
				if team:
					frappe.db.sql('''delete from `tabParticipating Teams` where name=%(name)s and parent=%(parent)s''',{'name':team[0].name,'parent':self.competition})

@frappe.whitelist()
def get_upcoming_events(doctype, txt, searchfield,filters, start=0, page_len=50):
	now = datetime.datetime.now()
	return frappe.db.sql("""select name from `tabEvents`
			where start_date > %(date)s			
			""".format(
				match_cond=get_match_cond(doctype),start=start,page_len=page_len), {"date": now	})

@frappe.whitelist()
def get_members(doctype, txt, searchfield,filters, start=0, page_len=50):
	ParticipatingMembers=frappe.db.sql("""select member from `tabEvent Participating Members`""")
	MembersList=frappe.db.sql("""select name from `tabMember`""")
	content=[]
	for x in MembersList:
		if ParticipatingMembers:	
			for y in ParticipatingMembers:
				if y!=x:
					content.append(x)
		else:
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
	teams=frappe.db.get_all('Participating Teams',filters={'parent':parent})
	idx=1
	if teams:
		idx=idx+len(teams)
	result=frappe.get_doc({
		"doctype":"Participating Teams","parent":parent,"parentfield":"table_11","parenttype":"Competition",
		"team":name,"age_group":age_group,"performance_duration":performance_duration,"team_head":teamhead,
		"no_of_participants":no_of_participants,"team_name":team,"idx":idx
		}).insert()
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
		self.flag='yes'
		if self.status=='Finalized':
			self.status='Approved'
		# if self.status=='Approved':
		# 	self.status='Waiting for approval'
	else:
		self.flag=''
	if(tableLength>settings[0].maximum_participants):
		frappe.throw(frappe._("Maximum of {0} participants are required ").format(settings[0].maximum_participants))	
	team_head=''
	for m in self.table_11:
		m.reg_competition=self.competition
		if m.member_type==settings[0].team_head:
			team_head=m.member			
	teamHead=frappe.db.get_all('Event Managing Team',fields=['member','member_type','parent'],
			filters={'member':team_head,'reg_competition':self.competition,'member_type':settings[0].team_head})	
	checkVal=[]
	for x in teamHead:
		if x.parent != self.name:
			checkVal.append(x)
	if checkVal:
		if len(checkVal)>=settings[0].max_team_head:
			frappe.throw(frappe._("Maximum of {0} teams can be handled by a single {1}")
				.format(settings[0].max_team_head,settings[0].team_head))

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
	# for x in self.table_11:		
	# 	if x.active=="In Active":
	# 		frappe.throw(frappe._('Member {0} - {1} is not active. Please renew the membership to participate in the event').format(x.member,x.member_name))
	for x in self.table_7:		
		if x.active=="In Active" or x.active=="InActive":
			x.prize_type='None'		
			# frappe.throw(frappe._('Member {0} - {1} is not active. Please renew the membership to participate in the event').format(x.member,x.member_name))
		for y in self.table_7:
			if x.name!=y.name and x.member==y.member:
				frappe.throw(frappe._('Member {0} - {1} is already added in the team').format(x.member,x.member_name))

@frappe.whitelist()
def assign_role(team_head,check_role):	
	if check_role==0:
		user=frappe.db.get_all('Member',fields=['email'],filters={'name':team_head})[0]
		result= frappe.get_doc({
			"doctype": "Has Role","name": nowdate(),"parent": user.email,"parentfield": "roles",
			"parenttype": "User","role": 'Choreographer'
			}).insert()

@frappe.whitelist()
def validate_trophy(self):
	trophy_setting=frappe.get_doc("General Settings", "General Settings")	
	for x in self.table_7:
		if x.prize_type=="Trophy":
			participant=[]
			participants=frappe.db.get_all('Event Participating Members',fields=['prize_type','member','parent']
				,filters={'member':x.member,'prize_type':'Trophy'})
			for data in participants:
				if data.parent!=self.name:
					participant.append(data)
			member=frappe.db.get_all('Member',fields=['date_of_birth'],filters={'name':x.member})
			now = datetime.date.today()
			birth=member[0].date_of_birth
			age=now.year - birth.year - ((now.month, now.day) < (birth.month, birth.day))			
			if age:
				if int(age)<int(trophy_setting.trophy_age_limit):
					if int(trophy_setting.no_of_trophy)>0:
						if len(participant)>=int(trophy_setting.no_of_trophy):
							frappe.throw(frappe._('Trophy limit exceede for member {0} - {1}. Only {2} trophies are allowed for member below {3} years of age').format(x.member,x.member_name,trophy_setting.no_of_trophy,trophy_setting.trophy_age_limit))
				else:
					frappe.throw(frappe._('Trophy is not allowed for member {0} - {1}. Trophies are only allowed for members below {2} years of age.').format(x.member,x.member_name,trophy_setting.trophy_age_limit))
@frappe.whitelist()
def validate_age_group(self):
	age_group=self.age_group
	age_group_limit=frappe.db.get_all('Age Group',fields=['from_age','to_age'],filters={'name':age_group})[0]	
	now = datetime.date.today()
	if self.table_7:
		for x in self.table_7:
			member=frappe.db.get_all('Member',fields=['date_of_birth'],filters={'name':x.member})			
			birth=member[0].date_of_birth
			age=now.year - birth.year - ((now.month, now.day) < (birth.month, birth.day))	
			if age_group_limit.from_age>0 and age_group_limit.to_age>0:
				if age<age_group_limit.from_age or age>age_group_limit.to_age:
					frappe.throw(frappe._('Member {0} - {1} does not fall under the selected age group. Please select different member or select "All Age" in age group').format(x.member,x.member_name))
			elif age_group_limit.from_age>0 and age_group_limit.to_age==0:
				if age<age_group_limit.from_age:
					frappe.throw(frappe._('Member {0} - {1} does not fall under the selected age group. Please select different member or select "All Age" in age group').format(x.member,x.member_name))
@frappe.whitelist()
def validate_song_background(self):
	if self.table_15:
		for x in self.table_15:
			if x.from_time.find(':')==-1:
				frappe.throw(frappe._('From Time should be in the format MM:SS at Row {0}').format(x.idx))
			if x.to_time.find(':')==-1:
				frappe.throw(frappe._('To Time should be in the format MM:SS at Row {0}').format(x.idx))
			if x.color_code:
				if x.color_code.find(',')!=-1:
					frappe.throw(frappe._('Please enter only one color code at Row {0}').format(x.idx))
				if len(x.color_code)!=7:
					frappe.throw(frappe._('Please enter valid color code at Row {0}').format(x.idx))
				strg="#"
				if x.color_code.count(strg)>1:
					frappe.throw(frappe._('More than 1 # tag is specified in the color code at Row {0}').format(x.idx))
				elif x.color_code.count(strg)==0:
					frappe.throw(frappe._('# tag is not included in the color code at Row {0}').format(x.idx))
@frappe.whitelist()
def check_role(self,team_head_id):	
	user=frappe.db.get_all('Member',fields=['email','name'],filters={'name':team_head_id})
	if user:
		email=user[0].email if user[0].email else user[0].name.lower()+"@gsod.org"
		roles=frappe.db.get_all('Has Role',fields=['parent','role'],filters={'parent':email,'role':'Choreographer'})
		if roles:
			return 1
		else:
			return 0
	else:
		return 0																				
