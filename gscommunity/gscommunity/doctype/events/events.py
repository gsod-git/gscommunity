# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import calendar
from frappe.website.website_generator import WebsiteGenerator
from frappe.website.utils import clear_cache
from frappe.utils import getdate,datetime,nowdate
from datetime import date
# from frappe.website.utils import get_page_context

class Events(WebsiteGenerator):
	def autoname(self):		
		self.name = self.name1.replace('&','and')

	def on_update(self):
		clear_cache()
		if self.venue_type=='Event Hall':
			if not self.event_venue:
				frappe.throw(frappe._('Please select event venue'),frappe.PermissionError)		

	def validate(self):
		if not self.route:
			self.route = '/'+self.scrub(self.name)
		super(Events, self).validate()


	def get_context(self,context):		
		EventsList=frappe.db.get_all('Events',fields=['*'], filters={'name':self.name})
		for item in EventsList:
			item.dates=getdate(item.start_date).strftime("%d") 
			item.months = frappe.utils.formatdate(item.start_date, "MMM YYYY")
			if item.end_date:
				item.end_dates=getdate(item.end_date).strftime("%d") 
				item.end_months = frappe.utils.formatdate(item.end_date, "MMM YYYY")
			item.days = calendar.day_name[item.start_date.weekday()] 
			item.eventtimings = frappe.db.get_all('Event Timeline'
				,fields=['title','date','from_time','to_time']
				, filters={'parent':item.name},order_by='idx')
			if item.venue_type=='Event Hall':
				if item.event_venue:
					venue_detail=frappe.db.get_all('Event Halls'
						,fields=['name','address_line_1','address_line_2','city','state','zip_code'],
						filters={'name':item.event_venue})[0]
					item.location=venue_detail.address_line_1
					item.address_line_2=venue_detail.address_line_2
					item.city=venue_detail.city
					item.state=venue_detail.state
					item.zip_code=venue_detail.zip_code
		context.EventsList = EventsList 
		context.title=self.name
		RightWidget=get_widgets('Sponsors','Right Panel','List View') 
		context.RightWidget = RightWidget
		Competition=frappe.db.get_all('Competition',fields=['name','events','competition_type','registration_start_date','registration_end_date'],
				filters={'events':self.name})
		now=datetime.date.today()
		content=[]
		for item in Competition:
			if(item.registration_start_date <= now and item.registration_end_date>=now):
				content.append(item)
		context.Competition=content
		context.test=Competition		
		Survey=frappe.db.get_all('Event Survey',fields=['name','title','start_date','end_date','route','view_response_by'],
				filters={'events':self.name})		
		survey1=[]
		for item in Survey:
			if item.start_date<=now and item.end_date>=now:
				survey1.append(item)
		if survey1:	
			context.Survey=survey1[0]
		Sponsorship=frappe.db.get_all('Sponsorship Items',fields=['name','item_name','item_amount','validity'],
			filters={'sponsor_for':self.name},order_by='display_id')
		for data in Sponsorship:
			data.features=frappe.db.get_all('Sponsor Features',fields=['features'],filters={'parent':data.name})
		context.Sponsorship=Sponsorship
		settings=frappe.get_single('General Settings')
		context.booking_url=settings.event_booking_url	

def get_widgets(category,position,view):
	Widget=frappe.db.get_all('Widget Placeholder', fields=['title','category','view','name','position'],filters={'view':view,'category':category,'position':position})
	for item in Widget:
		Widgets=frappe.db.get_all('Widget Config', fields=['widget_name','widget_type','html_content','max_data','link_data','sort_order'],order_by='sort_order',filters={'parent':item.name})
		for data in Widgets:
			Content=[];			
			if data.widget_type=='Dynamic':				
				if data.link_data=='Sponsors':
					RelatedData=frappe.db.get_all(data.link_data,fields=['sponsor_name','company_name','logo'],order_by='name desc',limit_page_length=data.max_data)
					Content.append(RelatedData) 

				else:
					RelatedData=frappe.db.get_all(data.link_data,fields=['title','route'])
					Content.append(RelatedData)
			data.Content=Content	 
		item.Widgets=Widgets
	return Widget

@frappe.whitelist(allow_guest=True)
def get_events():
	Events = frappe.db.get_all('Events',fields=['name'], filters={'published':1})
	return Events	

@frappe.whitelist(allow_guest=True)
def add_pagecount(name,pagecount): 
	if name and frappe.db.exists('Events', name):
		sno = frappe.get_doc('Events', name)
		sno.view_count = pagecount
		sno.db_update()

@frappe.whitelist(allow_guest=True)
def add_event_volunteer(member,event):
	volunteer=frappe.db.get_all('Volunteer',fields=['name','member','member_name']
		,filters={'member':member})
	result=''
	if volunteer:		
		check_volunteer=frappe.db.get_all('Event Volunteer',fields=['name'],filters={'volunteer':volunteer[0].name,'parent':event})

		if not check_volunteer:
			frappe.db.sql("""insert into `tabEvent Volunteer`
				(name,parent,parentfield,parenttype,volunteer,volunteer_name) 
				values(%(name)s,%(parent)s,%(parentfield)s,%(parenttype)s,%(volunteer)s,%(volunteer_name)s) """
   					.format(),{
   					"name":get_random(),
   					"parent":event,
   					"parentfield":"table_29",
   					"parenttype":"Events",
   					"volunteer":volunteer[0].name,
   					"volunteer_name":volunteer[0].member_name
   					})
			result='Success'
		else:
			result='Already Registered'
	else:
		result='0'
	return result

@frappe.whitelist()
def get_random():
	import random 
	import string
	random = ''.join([random.choice(string.ascii_letters
            + string.digits) for n in range(12)])
	Name=frappe.db.get_all('Event Volunteer',fields=['name','parent'])
	for x in Name:
		if x.name==random:
			random=get_random()
	return random
@frappe.whitelist(allow_guest=True)
def get_choreographer_details(competition,member):	
	if frappe.session.user!='Guest' and frappe.session.user!='Administrator':
		comp=frappe.db.get_value('Competition',competition,'max_team_head')
		ret=0
		role=frappe.db.get_all('Has Role',fields=['role'],filters={'parent':frappe.session.user,'role':'Choreographer'})
		team=frappe.db.get_all('Event Managing Team',fields=['name'],filters={'reg_competition':competition,'member':member})
		# if role:			
		content=[]
		content.append({'comp':comp,'team':len(team)})
		return content[0]	
