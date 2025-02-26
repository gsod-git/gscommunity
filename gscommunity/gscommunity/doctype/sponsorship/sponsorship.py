# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import getdate, add_months, add_to_date,nowdate
from frappe.website.utils import clear_cache
from datetime import date,datetime

class Sponsorship(Document):
	def on_update(self):
		settings=frappe.get_doc("General Settings", "General Settings")
		self.expires_on=settings.expiry_date		
		if self.sponsor_type=="Guest":
			if self.sponsor_name and self.email and self.phone:
				add_user(self.sponsor_name,self.email,self.phone,self.last_name)
			set_expiry(self,settings)
		else:
			if self.member:
				member=frappe.db.get_all('Member',fields=['membership_type','membership_expiry_date'],filters={'name':self.member})
				set_expiry(self,settings)
		if self.paid:
			self.active=1
			yellowpage=frappe.db.get_list('Yellow Pages',filters={'sponsor':self.name},fields=['*'])
			if yellowpage:
				for item in yellowpage:
					if item.status!='Waiting for approval':
						frappe.set_value('Yellow Pages',item.name,'published',1)
					else:
						frappe.set_value('Yellow Pages',item.name,'published',0)

	def get_context(self,context): 
		SponsorsList=frappe.db.get_all('Sponsorship', fields=['name','route','company_name','logo','sponsorship_type','starts_on','expires_on','website_url','phone','email','address','description'], filters={'name':self.name})
		context.SponsorsList=SponsorsList 
		context.title=self.name
@frappe.whitelist(allow_guest=True)
def set_expiry(self,settings):
	if self.sponsorship_type=='Events':
		sponsor=frappe.db.get_all('Sponsorship Items',fields=['sponsor_for'],filters={'sponsorship_type':self.sponsorship_type})
		event=frappe.db.get_all('Events',fields=['*'],filters={'name':sponsor[0].sponsor_for})
		if event[0].end_date:
			self.expires_on=event[0].end_date
		else:
			self.expires_on=event[0].start_date
	elif self.sponsorship_type=='Samaj Darshan':
		month=self.sponsorship_plan.split('-')[0]
		year=self.sponsorship_plan.split('-')[1]
		if month=='All (Jan to Dec)':
			self.expires_on=settings.expiry_date
		else:
			month_no=get_month(month)
			day=30
			if(month_no==2):
				day=28
			year=int(year)
			expiry_date=datetime(year,month_no,day)
			self.expires_on=expiry_date
	else:
		self.expires_on=settings.expiry_date

@frappe.whitelist(allow_guest=True)
def add_months(date, months,sponsorship_type,sponsorship_plan):
	if sponsorship_type=='General':
		return add_to_date(date, months=int(months))
	elif sponsorship_type=='Events':
		event=frappe.db.get_all('Sponsorship Items',fields=['sponsor_for'],filters={'name':sponsorship_plan})
		event_detail=frappe.db.get_all('Events',fields=['start_date','end_date'],filters={'name':event[0].sponsor_for})
		if event_detail[0].end_date:
			return event_detail[0].end_date
		else:
			return event_detail[0].start_date

@frappe.whitelist()
def get_sponsorship_items(doctype, txt, searchfield,filters, start=0, page_len=50):
	SponsorshipItems=frappe.db.get_all('Sponsorship Items',fields=['name'],filters={"sponsorship_type":txt})	
	return SponsorshipItems

@frappe.whitelist()
def get_yellowpage_detail(name):
	yp=frappe.db.get_all('Yellow Pages',fields=['*'],filters={'sponsor':name})
	if yp:
		return yp
	else:
		return '0'
@frappe.whitelist()
def get_advertisement_detail(name):
	ad=frappe.db.get_all('GSOD Promotions',fields=['*']
		,filters={'sponsor':name})
	if ad:
		return ad
	else:
		return '0'
@frappe.whitelist(allow_guest=True)
def add_user(name,email,phone,last_name):
	if not frappe.db.get_value("User", email):
		result= frappe.get_doc({
			"doctype": "User","email": email,"first_name": name,"mobile_no":phone,"send_welcome_email":1,
			"last_name":last_name
		}).insert()
		add_role(email)
		
@frappe.whitelist(allow_guest=True)
def add_role(email):
	frappe.get_doc({
			"doctype": "Has Role","name": nowdate(),"parent": email,"parentfield": "roles",
			"parenttype": "User","role": "Web User"
		}).insert()
@frappe.whitelist()
def add_yellow_page(b_name,b_type,sponsor,category,subcategory,email,phone,address,city,state,zip_code,published):
	result=frappe.get_doc({
		"doctype":"Yellow Pages","name":b_name,"business_name":b_name,"business_type":b_type,
		"sponsor":sponsor,"category":category,"subcategory":subcategory,"address":address,
		"city":city,"state":state,"zip_code":zip_code,"published":published,"view_count":0,
		"website_url":''
		}).insert()
	return result
@frappe.whitelist()
def add_advertisement(ad_name,redirect_url,sponsor,start_date,end_date,published,sponsorship_plan,sponsorship_type):
	plan=frappe.db.get_all('Sponsorship Type',fields=['advertisement_timing'],filters={'name':sponsorship_type})
	result=frappe.get_doc({
		"doctype":"GSOD Promotions","name":ad_name,"advertisement_name":ad_name,"start_date":start_date,
		"end_date":end_date,"published":published,"redirect_url":redirect_url,
		"slot_timing":plan[0].advertisement_timing,"sponsor":sponsor,"views":0,"status":'Waiting for approval'	
		}).insert()
	return result
@frappe.whitelist(allow_guest=True)
def make_payment(docname,email,amount,transaction_id,payment_date=None):
	sponsorship=frappe.db.get_all('Sponsorship',fields=['member','email','amount','sponsorship_plan'],filters={'name':docname})
	if sponsorship:
		sponsorship_plan=frappe.db.get_all('Sponsorship Items',fields=['accounting_head'],filters={'name':sponsorship[0].sponsorship_plan})
		if not frappe.db.get_value("Payment Entries", docname):
			if sponsorship[0].member:
				frappe.get_doc({
					"doctype": "Payment Entries",
					"payment_date": payment_date if payment_date else getdate(nowdate()),
					"payment_for": "Sponsorship",
					"ref_id": docname,
					"member": sponsorship[0].member,
					"paid_amount":sponsorship[0].amount,
					"mode_of_payment":"Online Payment",
					"accounting_head":sponsorship_plan[0].accounting_head,
					"payment_type":"Credit"
				}).submit()
			else:
				frappe.get_doc({
					"doctype": "Payment Entries",
					"payment_date": payment_date if payment_date else getdate(nowdate()),
					"payment_for": "Sponsorship",
					"ref_id": docname,
					"user": sponsorship[0].email,
					"paid_amount":sponsorship[0].amount,
					"mode_of_payment":"Online Payment",
					"transaction_id":transaction_id,
					"accounting_head":sponsorship_plan[0].accounting_head
				}).submit()
	if frappe.db.get_value("Sponsorship", docname):	
		doc=frappe.get_doc('Sponsorship',docname)
		doc.paid=1
		doc.published=1
		doc.docstatus=1
		doc.save()
	yp=frappe.db.get_all('Yellow Pages',fields=['name','status'],filters={'user':sponsorship[0].email})
	# ads=frappe.db.get_all('Advertisement',fields=['name','status'],filters={'sponsor':sponsorship[0].name})
	# if ads:
	# 	if ads.status!='Waiting for approval':
	# 		frappe.db.set_value("Advertisement", ads[0].name , "published", 1)
	# 	frappe.db.set_value("Advertisement", ads[0].name , "published_on", nowdate())
	sponsorlist=frappe.db.sql('''select s.name,s.email,s.expires_on from `tabSponsorship` s left join `tabSponsorship Type` st on s.sponsorship_type=st.name where st.enable_yellowpage=1 and s.email=%(email)s order by s.expires_on desc''',{'email':sponsorship[0].email},as_dict=1)
	if sponsorlist:
		if yp:
			if yp[0].status!='Waiting for approval':
				frappe.db.set_value("Yellow Pages", yp[0].name , "published", 1)
			frappe.db.set_value("Yellow Pages", yp[0].name , "sponsor", sponsorlist[0].name)
			frappe.db.set_value("Yellow Pages", yp[0].name , "expires_on", sponsorlist[0].expires_on)
	else:
		if yp[0].status!='Waiting for approval':
			frappe.db.set_value("Yellow Pages", yp[0].name , "published", 1)
		frappe.db.set_value("Yellow Pages", yp[0].name , "sponsor", sponsorship[0].name)
		frappe.db.set_value("Yellow Pages", yp[0].name , "expires_on", sponsorship[0].expires_on)

@frappe.whitelist(allow_guest=True)
def get_expiry_date(sponsorship_type,sponsorship_plan,member):
	settings=frappe.get_doc("General Settings", "General Settings")
	# expires_on=settings.expiry_date				
	# if member:
	# 	member=frappe.db.get_all('Member',fields=['membership_type','membership_expiry_date'],filters={'name':member})		
	# 	if member[0].membership_type==settings.membership_type:
	# 		expires_on=member[0].membership_expiry_date
	# 	else:
	# 		expires_on=get_validity(sponsorship_type,sponsorship_plan)
	# else:
	expires_on=get_validity(sponsorship_type,sponsorship_plan)
	return expires_on

@frappe.whitelist(allow_guest=True)
def get_validity(sponsorship_type,sponsorship_plan):
	settings=frappe.get_doc("General Settings", "General Settings")
	expires_on=settings.expiry_date	
	if sponsorship_type=='Events':
		sponsor=frappe.db.get_all('Sponsorship Items',fields=['sponsor_for'],filters={'name':sponsorship_plan})		
		event=frappe.db.get_all('Events',fields=['*'],filters={'name':sponsor[0].sponsor_for})
		if event[0].end_date:
			expires_on=event[0].end_date
		else:
			expires_on=event[0].start_date
	elif sponsorship_type=='Samaj Darshan':
		month=sponsorship_plan.split('-')[0]
		year=sponsorship_plan.split('-')[1]
		if month=='All (Jan to Dec)':
			expires_on=settings.expiry_date
		else:
			month_no=get_month(month)
			day=30
			if(month_no==2):
				day=28
			year=int(year)
			expiry_date=date(year,month_no,day)
			expires_on=expiry_date
	return expires_on
@frappe.whitelist(allow_guest=True)
def get_month(month):
	if month=='January':
		return 1
	elif month=='February':
		return 2
	elif month=='March':
		return 3
	elif month=='April':
		return 4
	elif month=='May':
		return 5
	elif month=='June':
		return 6
	elif month=='July':
		return 7
	elif month=='August':
		return 8
	elif month=='September':
		return 9
	elif month=='October':
		return 10
	elif month=='November':
		return 11
	elif month=='December':
		return 12