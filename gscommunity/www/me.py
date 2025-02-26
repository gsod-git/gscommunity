# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import frappe.www.list
import datetime
from datetime import date, datetime, time
from frappe.utils import flt, today, getdate

no_cache = 1
no_sitemap = 1

def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	context.show_sidebar=True
	Userdetails=frappe.get_doc('User',frappe.session.user)
	context.Userdetails=Userdetails
	if frappe.session.user!='Administrator':
		context.user=frappe.session.user
		if 'MEM-' in Userdetails.username:		
			MemberInfo=frappe.get_doc('Member',Userdetails.username)
			MemberInfo=get_family_details(MemberInfo)
			context.MemberInfo=MemberInfo
			context.active=MemberInfo.active
			context.show_free_yp=get_yp_details(MemberInfo)
		else:
			Info=frappe.db.get_list('Member', fields=['*'], filters={'email':Userdetails.email})
			if Info:
				MemberInfo=Info[0]
				MemberInfo=get_family_details(MemberInfo)		
				context.MemberInfo=MemberInfo
				context.active=MemberInfo.active
				context.show_free_yp=get_yp_details(MemberInfo)	
			
def get_family_details(MemberInfo):
	if MemberInfo:
		if MemberInfo.membership_expiry_date:
			newdate1=date.today()
			newdate2=MemberInfo.membership_expiry_date
			if newdate1 >= newdate2:
				MemberInfo.mstatus=1
				frappe.db.set_value('Member',MemberInfo.name,'active',0)	
			else:
				MemberInfo.mstatus=2
		else:
			MemberInfo.mstatus=0
		MemberInfo.FamilyInfo=frappe.db.get_all('Other Members', fields=['*'], filters={'parent':MemberInfo.name})
	return MemberInfo
def get_yp_details(MemberInfo):
	settings=frappe.get_doc("General Settings", "General Settings")
	yp_setting=frappe.db.get_all('Yellowpage Setting',fields=['*'],filters={'membership_type':MemberInfo.membership_type})
	show_free_yp=0
	if yp_setting:
		yp_enable=yp_setting[0].free_yellowpage
		if yp_enable:
			yp=frappe.db.get_all('Yellow Pages',fields=['*'],filters={'user':frappe.session.user})
			if yp:
				show_free_yp=0
			else:
				show_free_yp=1
	return show_free_yp