# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
# import frappe
# from _future_ import unicode_literals
import frappe
import frappe.utils
import json
import calendar
from frappe import _
from frappe.utils import getdate,nowdate
from datetime import date
 

def get_context(context):
	now=getdate(nowdate())
	GeneralSponsorType=frappe.db.sql('''select distinct sponsorship_type from `tabSponsorship Items` where sponsor_for is null order by creation''',as_dict=1)
	loop_value=1
	for stype in GeneralSponsorType:
		SponsorItem=frappe.db.get_all('Sponsorship Items',fields=['*'],filters={'sponsorship_type':stype.sponsorship_type},order_by='display_id')
		for item in SponsorItem:
			item.features=frappe.db.get_all('Sponsor Features',fields=['features'],filters={'parent':item.name})
		stype.SponsorItem=SponsorItem
		stype.loop_value=loop_value
		loop_value=loop_value+1
	context.GeneralSponsorType=GeneralSponsorType
	context.title='Sposorship Types'
	SponsorTypes=frappe.db.sql('''select distinct sponsorship_type from `tabSponsorship Items` where sponsor_for is not null order by creation''',as_dict=1)
	for stype in SponsorTypes:
		sponsor_for=frappe.db.sql('''select distinct sponsor_for from `tabSponsorship Items` where sponsorship_type=%(sponsor_type)s''',{'sponsor_type':stype.sponsorship_type},as_dict=1)
		item=[]
		if stype.sponsorship_type=='Events':
			events=frappe.db.sql('''select name from tabEvents where start_date>=%(now)s''',{'now':now},as_dict=1)			
			for event in events:
				for s_item in sponsor_for:
					if event.name==s_item.sponsor_for:
						item.append(event)			
		elif stype.sponsorship_type=='Samaj Darshan':
			samaj_list=[]
			year=now.year
			samajd=frappe.db.sql('''select * from `tabSamaj Darshan` where year>={year} order by year desc'''.format(year=year),as_dict=1)
			for l in samajd:
				samaj_darshan=frappe.db.get_all('Samaj Darshan Lists',fields=['*'],filters={'published':0,'parent':l.name},order_by='idx')
				for sd in samaj_darshan:
					samaj_list.append(sd)			
			for samaj in samaj_list:
				samaj.s_year=samaj.parent.split(' ')[2]
				samaj.name=samaj.month+'-'+samaj.s_year
				for s_item in sponsor_for:
					if samaj.name==s_item.sponsor_for:
						item.append(samaj)			
		for data in item:				
			SponsorItem=frappe.db.get_all('Sponsorship Items',fields=['*'],filters={'sponsorship_type':stype.sponsorship_type,'sponsor_for':data.name},order_by='display_id')
			for s_item in SponsorItem:				
				s_item.features=frappe.db.get_all('Sponsor Features',fields=['features'],filters={'parent':s_item.name})				
			data.SponsorItem=SponsorItem				
		stype.Type=item
		stype.loop_value=loop_value
		loop_value=loop_value+1
	context.SponsorTypes=SponsorTypes