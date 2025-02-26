from __future__ import unicode_literals

import frappe
from frappe.utils import nowdate
import datetime
from datetime import date, datetime, time
from frappe.utils import getdate,nowdate

def get_context(context):
	# do your magic here
	pass

@frappe.whitelist(allow_guest=True)
def get_sponsor_plan(stype):
	s_plan=frappe.db.get_all('Sponsorship Items',fields=['name','item_name','validity','accounting_head'],filters={'sponsorship_type':stype})
	return s_plan
@frappe.whitelist(allow_guest=True)
def get_plan_amount(sptype):
	s_plan=frappe.db.get_all('Sponsorship Items',fields=['name','item_name','item_amount','validity','accounting_head'],filters={'name':sptype})
	return s_plan
@frappe.whitelist(allow_guest=True)
def get_member_info(phone,email):
	if email!='':
		member=frappe.db.get_all('Member',fields=['name','member_name','active','email','phone_no','last_name'],
			filters={'email':email})
	elif phone!='':
		member=frappe.db.get_all('Member',fields=['name','member_name','active','email','phone_no','last_name'],
			filters={'phone_no':phone})
	if member:
		return member[0]
	else:
		return '0'
@frappe.whitelist(allow_guest=True)
def add_new_yellowpage(b_name,b_type,category,sub_category,addr_1,addr_2,city,state,zip,owner_name,email,phone,fax,name):
	if frappe.db.get_value("Yellow Pages", name):
		doc=frappe.get_doc('Yellow Pages',name)
		doc.business_name=b_name
		doc.business_type=b_type
		doc.category=category
		doc.subcategory=sub_category
		doc.email=email
		doc.phone=phone
		doc.fax=fax
		doc.address=addr_1
		doc.address_line_2=addr_2
		doc.city=city
		doc.state=state
		doc.zip_code=zip
		doc.save()		
	else:
		sponsor=frappe.get_last_doc('Sponsorship')
		route=b_name.lower().replace(' ','-')		
		result=frappe.get_doc({
			"doctype":"Yellow Pages","business_name":b_name,"business_type":b_type,"category":category,
			"subcategory":sub_category,"owner_name":owner_name,"email":email,"phone":phone,"fax":fax,
			"address":addr_1,"address_line_2":addr_2,"city":city,"state":state,"zip_code":zip,"view_count":0,
			"status":"Waiting for approval","route":route,"sponsor":sponsor.name,"user":frappe.session.user
			}).insert()

			
@frappe.whitelist(allow_guest=True)
def get_sponsor_feature(plan):
	plan=frappe.db.get_all('Sponsorship Items',fields=['sponsorship_type'],filters={'name':plan})
	return frappe.db.get_all('Sponsorship Type',fields=['enable_yellowpage'],filters={'name':plan[0].sponsorship_type})

@frappe.whitelist(allow_guest=True)
def update_sponsor(name,yp,yp_name):
	if frappe.db.get_value("Sponsorship", name):
		now=getdate(nowdate())
		sponsor=frappe.db.get_all('Sponsorship',fields=['name','email','expires_on'],filters={'name':name})[0]
		sponsorlist=frappe.db.sql('''select s.name,s.email,s.expires_on from `tabSponsorship` s left join `tabSponsorship Type` st on s.sponsorship_type=st.name where st.enable_yellowpage=1 and s.email=%(email)s order by s.expires_on desc''',{'email':sponsor.email},as_dict=1)
		if yp_name:
			if sponsorlist:		
				update_yp(yp_name,sponsorlist[0].name,sponsorlist[0].email,sponsorlist[0].expires_on)
			else:
				update_yp(yp_name,sponsor.name,sponsor.email,sponsor.expires_on)
		else:
			if sponsorlist:
				update_yp(yp,sponsorlist[0].name,sponsorlist[0].email,sponsorlist[0].expires_on)
			else:
				update_yp(yp_name,sponsor.name,sponsor.email,sponsor.expires_on)
@frappe.whitelist(allow_guest=True)
def update_yp(name,sponsor,email,expires_on):
	frappe.db.set_value("Yellow Pages", name , "sponsor", sponsor)	
	frappe.db.set_value("Yellow Pages", name , "user", email)
	frappe.db.set_value("Yellow Pages", name , "expires_on", expires_on)
@frappe.whitelist(allow_guest=True)
def get_user(user):
	user=frappe.db.get_all('User',fields=['*'],filters={'name':user})
	if user:
		return user[0]
@frappe.whitelist(allow_guest=True)
def add_user(name,email,phone):
	if not frappe.db.get_value("User", email):
		result= frappe.get_doc({
			"doctype": "User",
			"email": email,
			"first_name": name,
			"mobile_no":phone,
			"send_welcome_email":1
		}).insert()
		frappe.get_doc({
			"doctype": "Has Role",
			"name": nowdate(),
			"parent": email,
			"parentfield": "roles",
			"parenttype": "User",
			"role": "Web User"
		}).insert()
		sponsor=frappe.db.get_all('Sponsorship',fields='name',order_by='creation desc')[0]
		if frappe.db.get_value("Sponsorship", sponsor.name):	
			frappe.db.set_value("Sponsorship", name , "sponsor_type", 'Guest')
@frappe.whitelist(allow_guest=True)
def get_yellowpage(email):
	yellow_page=frappe.db.get_all('Yellow Pages',fields=['*'],filters={'user':email})
	return yellow_page
@frappe.whitelist(allow_guest=True)
def check_guest_details(email):
	member=frappe.db.get_all('Member',fields=['name'],filters={'email':email})
	if member:
		return member