from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import getdate,datetime
from datetime import date

def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	else:
		username=frappe.db.get_value('User',frappe.session.user,'username')
		member=frappe.db.get_all('Member',fields=['name','first_edit','primary_member_id'],filters={'name':username})
		if not member:
			frappe.throw(_("You need to be a member of GSOD to access this page"), frappe.PermissionError)
		else:
			if not member[0].primary_member_id: 
				if member[0].first_edit=="0":
					frappe.throw(_("You do not have permission to access this page"), frappe.PermissionError)

@frappe.whitelist(allow_guest=True)
def get_upcoming_events():
	now = datetime.datetime.now()
	return frappe.db.sql("""select name from `tabEvents`
			where start_date > %(date)s			
			""".format(), {					
					"date": now
				})
@frappe.whitelist(allow_guest=True)
def get_members():
	ParticipatingMembers=frappe.db.sql("""select member from `tabEvent Participating Members`""")
	MembersList=frappe.db.sql("""select name from `tabMember`""")
	content=[]
	for x in MembersList:
		for y in ParticipatingMembers:
			if y!=x:
				content.append(x)
	return content
@frappe.whitelist(allow_guest=True)
def get_songDuration(Competition):
	settings = frappe.db.get_all("Competition"
			,fields=['maximum_participants','minimum_participants','team_head','max_team_head','performance_duration'],
			filters={'name':competition})
	return settings[0].performance_duration
@frappe.whitelist(allow_guest=True)
def get_competition(name,team=''):
	competition=frappe.db.get_all("Competition"
			,fields=['competition_type','maximum_participants','minimum_participants','team_head','max_team_head','performance_duration'],
			filters={'name':name})
	if team!='':
		team_status=frappe.db.get_value("Team",team,"status")
		competition[0].team_status=team_status
	else:
		competition[0].team_status='Waiting for approval'
	return competition[0]
@frappe.whitelist(allow_guest=True)
def get_event_related_competition(events):
	return frappe.db.get_all('Competition',fields=['name','title'],filters={'events':events})
@frappe.whitelist(allow_guest=True)
def savedoc(fileurl,name,duration):
	result=frappe.db.sql("""update `tabTeam` set song=%(song)s,
		song_duration=%(duration)s where name=%(name)s"""
		.format(),{
		"song":fileurl,
		"name":name,
		"duration":duration
		})
	return result
@frappe.whitelist(allow_guest=True)
def getMember_details(name):
	return frappe.db.get_all('Member',fields=['member_name','active','mobile_no','email'],
		 	filters={'name':name})[0]
@frappe.whitelist(allow_guest=True)
def get_hall_color(events):
	# Colors=frappe.db.sql("""select name from `tabColors`""")
	EventHall=frappe.db.get_all('Events',fields=['event_venue'],filters={"name":events})
	if EventHall:
		for x in EventHall:
			Hall=frappe.db.get_all('Event Halls',fields=['name','any_color'],filters={"name":x.event_venue})
			if Hall and not Hall[0].any_color:
				Colors=frappe.db.sql("""select color from `tabHall Colors` where parent=%(name)s"""
					.format(),{"name":Hall[0].name})
				return Colors
			else:
				return 'All'
@frappe.whitelist(allow_guest=True)
def get_all_members(txt,start=0,limit=20):
	return frappe.db.get_all('Member',fields=['name','member_name','last_name','phone_no','email'])
@frappe.whitelist(allow_guest=True)
def member_search(text, start=0, limit=20):
	doctype='Member'
	text = text+"%"
	# results = frappe.db.sql('''
	# 	select
	# 		content, name
	# 	from
	# 		__global_search
	# 	where 
	# 		content like %s and doctype in ('Member')
	# 	limit {start}, {limit}'''.format(start=start,limit=limit),(text))
	results=frappe.db.sql('''select * from `tabMember` where (name like %(text)s or 
		concat(member_name,last_name) like %(text)s or email like %(text)s 
		or phone_no like %(text)s) order by member_name limit {limit}'''
		.format(limit=limit),{'text':text},as_dict=1)
	content=[]	
	for item in results:
		family=[]
		member_info=item
		address=member_info.city+', '+member_info.state
		if member_info.self_relation=='Self':
			if member_info.table_25:
				for f in member_info.table_25:
					name=f.member_name+' '+f.last_name
					family.append(name)
			content.append({'first_name':member_info.member_name,'last_name':member_info.last_name,'email':member_info.last_name,'phone_no':member_info.phone_no,'family':family,'address':address,'name':item.name})
		else:
			if frappe.db.get_value('Member',member_info.primary_member_id):
				primary_member=frappe.get_doc('Member',member_info.primary_member_id)
				p_name=primary_member.member_name+' '+primary_member.last_name
				family.append(p_name)
				if primary_member.table_25:
					for f in primary_member.table_25:
						if f.member_name!=member_info.member_name and f.date_of_birth!=member_info.date_of_birth:
							name=f.member_name+' '+f.last_name
							family.append(name)
				content.append({'first_name':member_info.member_name,'last_name':member_info.last_name,'email':member_info.last_name,'phone_no':member_info.phone_no,'family':family,'address':address,'name':item.name})
	return content
@frappe.whitelist(allow_guest=True)
def check_user(member):
	member=frappe.db.get_all('Member'
		,fields=['name','member_name','last_name','phone_no','mobile_no','email','active']
		,filters={'name':member})
	if member:	
		return member[0]
@frappe.whitelist(allow_guest=True)
def save_duration(doctype,docname,docfield,duration,file_name):
	result=frappe.db.get_all('File',fields=['file_url','file_name']
		,filters={'attached_to_doctype':doctype,'attached_to_name':docname,'attached_to_field':docfield})
	savedoc(file_name,docname,duration)
@frappe.whitelist(allow_guest=True)
def remove_file(doctype,docname,file_name):
	frappe.db.sql('''delete from `tabFile` where file_name=%(file_name)s and attached_to_name=%(docname)s and attached_to_doctype=%(doctype)s''',{'file_name':file_name,'docname':docname,'doctype':doctype})