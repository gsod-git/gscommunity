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
	SponsorshipTypeList=frappe.db.get_all('Sponsorship Items', fields=['name','item_name','ribbon_image','display_id']
		,filters={'sponsorship_type':'Advertising Plans'},order_by = "display_id")
	for data in SponsorshipTypeList:
		data.SponsorsBusinessList=frappe.db.get_all('Sponsorship', fields=['sponsor_name','sponsorship_plan','name','expires_on'], filters={'published': 1,'sponsorship_plan':data.name})
		for item in data.SponsorsBusinessList:
			if item.expires_on:
				if item.expires_on>=now:
					item.YellowpagesList=frappe.db.get_all('Yellow Pages', fields=['*'], filters={'published': 1,'status':'Approved','sponsor':item.name,'business_type':'Sponsor'})
				else:
					frappe.db.set_value("Sponsorship", item.name , "published", 0)
			# else:
			# 	item.YellowpagesList=frappe.db.get_all('Yellow Pages', fields=['*'], filters={'published': 1,'user':item.email,'business_type':'Sponsor','status':'Approved'})
	context.SponsorshipTypeList=SponsorshipTypeList
	YellowpagesList=frappe.db.get_all('Yellow Pages', fields=['*'], filters={'published': 1,'business_type':'Member','status':'Approved'})
	context.YellowpagesList=YellowpagesList
	context.title="Yellow Pages"
 
@frappe.whitelist(allow_guest=True)
def yellowpage_search(text, start=0, limit=20):
	text = "%"+text+"%"
	results = frappe.db.sql('''
		select
			content, name
		from
			__global_search
		where 
			content like %s and doctype in ('Yellow Pages')
		limit {start}, {limit}'''.format(start=start,limit=limit),(text))
	yp=[]
	yellowpages=frappe.db.get_all('Yellow Pages',filters={'published':1})
	for item in results:
		for yps in yellowpages:
			if yps.name==item[1]:
				yp.append(item)
	return yp	