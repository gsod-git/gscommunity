# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
# import frappe
# from _future_ import unicode_literals
import frappe
import frappe.utils
import json
from frappe import _
from frappe.utils import getdate,nowdate
from datetime import date


def get_context(context):
	now=getdate(nowdate())
	NewsList=frappe.db.get_all('Community News',fields=['name','published','route','date','facebook_link','youtube_link','image','description'], filters={'published':1}, order_by='date desc', limit_page_length=6)
	context.NewsList=NewsList	
	HomeSlider=frappe.db.get_all('HomeSliders',fields=['slidername','sub_title','imageurl','redirect_url'],filters={'show_in_website':1},order_by='displayorder')
	context.HomeSliders=HomeSlider 
	EventsList=frappe.db.sql('''select * from `tabEvents` where published=1 and (start_date>=%(now)s or end_date>=%(now)s) order by start_date limit 6'''.format(),{'now':now},as_dict=1)
	for item in EventsList:
		if len(item.name1)>35:
			item.name1=item.name1[:35]+'...'			
		if item.banner_image:
			item.image= frappe.db.get_all('File',fields=['thumb_file_1','thumb_file_2','file_url'],filters={'file_url':item.banner_image,'attached_to_doctype':'Events'})
		context.EventsList=EventsList
	GSODEventsList=frappe.db.sql('''select * from `tabEvents` where published=1 and (start_date>=%(now)s or end_date>=%(now)s) and event_type=%(event_type)s order by start_date limit 6''',{'now':now,'event_type':'GSOD Events'},as_dict=1)
	for item in GSODEventsList:
		if len(item.name1)>35:
			item.name1=item.name1[:35]+'...'	
		if item.banner_image:
			item.image= frappe.db.get_all('File',fields=['thumb_file_1','thumb_file_2','file_url'],filters={'file_url':item.banner_image,'attached_to_doctype':'Events'})
	GSSEventsList=frappe.db.sql('''select * from `tabEvents` where published=1 and (start_date>=%(now)s or end_date>=%(now)s) and event_type=%(event_type)s order by start_date limit 6''',{'now':now,'event_type':'GSS Events'},as_dict=1)
	for item in GSSEventsList:
		if len(item.name1)>35:
			item.name1=item.name1[:35]+'...'
		if item.banner_image:
			item.image= frappe.db.get_all('File',fields=['thumb_file_1','thumb_file_2','file_url'],filters={'file_url':item.banner_image,'attached_to_doctype':'Events'})
	GSYEventsList=frappe.db.sql('''select * from `tabEvents` where published=1 and (start_date>=%(now)s or end_date>=%(now)s) and event_type=%(event_type)s order by start_date limit 6''',{'now':now,'event_type':'GSY Events'},as_dict=1)
	for item in GSYEventsList:
		if len(item.name1)>35:
			item.name1=item.name1[:35]+'...'
		if item.banner_image:
			item.image= frappe.db.get_all('File',fields=['thumb_file_1','thumb_file_2','file_url'],filters={'file_url':item.banner_image,'attached_to_doctype':'Events'})
	context.GSYEventsList=GSYEventsList
	context.GSSEventsList=GSSEventsList
	context.GSODEventsList=GSODEventsList
	AlbumGroup=frappe.db.get_all('Event Group',fields=['name1','route'],filters={'published':1},order_by='name1')
	if "Member" in frappe.get_roles(frappe.session.user):
		member_cond=('in','Show to Members','Show to All') 
	else:
		member_cond='Show to All'
	for item in AlbumGroup:
		item.ShowAllAlbumsList=frappe.db.get_all('Gallery',fields=['events','event_date','route','name','cover_image'],filters={'published':1,'event_group':item.name1,'visibility':member_cond},order_by='creation desc')
		item.ShowToMemberAlbumsList=frappe.db.get_all('Gallery',fields=['events','event_date','route','name','cover_image'],filters={'published':1,'event_group':item.name1,'visibility':member_cond},order_by='creation desc')
		item.RecentAlbumsList=frappe.db.get_all('Gallery',fields=['events','event_date','route','name','cover_image'],filters={'published':1,'visibility':member_cond},order_by='creation desc')
		if item.cover_image:
			item.image= frappe.db.get_all('File',fields=['thumb_file_1','thumb_file_2','file_url'],filters={'file_url':item.cover_image,'attached_to_doctype':'Gallery'})
	context.AlbumGroup=AlbumGroup 
	RecentAlbumsList=frappe.db.get_all('Gallery',fields=['events','event_date','route','name','cover_image'],filters={'published':1,'visibility':member_cond},order_by='creation desc',limit_page_length=4)
	context.RecentAlbumsList=RecentAlbumsList 
	MembershipType=frappe.db.get_all('Membership Type',fields=['membership_type','amount','membership_info'])
	Member=[]
	for row in MembershipType:
		if(row.membership_type.find('-')==-1):
			Member.append(row)
		elif(row.membership_type.find('New')!=-1):
			row.membership_type=row.membership_type.split('-')[0]
			Member.append(row)
	context.MembershipType=Member
	context.title="GSOD"
	# settings=frappe.get_single('General Settings')
	# context.song=settings.audio