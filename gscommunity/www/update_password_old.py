# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
# import frappe
# from future import unicode_literals
import frappe
import frappe.utils
import json
from frappe import _
import frappe.www.list
from frappe.auth import LoginManager
from frappe.integrations.doctype.ldap_settings.ldap_settings import get_ldap_settings
from frappe.utils.password import get_decrypted_password

no_sitemap = 1
no_cache = 1

@frappe.whitelist(allow_guest=True)
def get_context(context):
	
	if frappe.session.user!='Guest' and frappe.session.user=='Administrator':
		context.Userdetails=frappe.db.get_list('User', fields=["username","first_name","full_name","email","last_name","username","gender","mobile_no","birth_date","location"], filters={'username':frappe.session.user})
		Data=Userdetails[0].email
		context.Userdetails=Userdetails
		context.Rdata=frappe.db.get_list('Member', fields=["name","member_name","membership_type","email","gender","active","last_name","membership_expiry_date","phone_no","date_of_birth"], filters={'email':Data})
		context.YellowpagesList=frappe.db.get_all('Yellow Pages', fields=['business_name','route','business_type','category','subcategory','owner_name','email','address','phone','image','description'], filters={'owner':frappe.session.user})
		context.show_sidebar=True
		context.no_breadcrumbs = True
		context.parents = [{"name":"me", "title":_("My Account")}]
	if frappe.session.user!='Guest' and frappe.session.user!='Administrator':
		Userdetails=frappe.db.get_list('User', fields=["first_name","full_name","email","last_name","username","gender","mobile_no","birth_date","location"], filters={'email':frappe.session.user})
		Data=Userdetails[0].email
		context.Userdetails=Userdetails
		context.Rdata=frappe.db.get_list('Member', fields=["name","member_name","membership_type","email","gender","active","last_name","membership_expiry_date","phone_no","date_of_birth"], filters={'email':Data})
		context.YellowpagesList=frappe.db.get_all('Yellow Pages', fields=['business_name','route','business_type','category','subcategory','owner_name','email','address','phone','image','description'], filters={'owner':frappe.session.user})
		context.show_sidebar=True
		context.no_breadcrumbs = True
		context.parents = [{"name":"me", "title":_("My Account")}]
	if frappe.session.user=='Guest':
		Key=frappe.form_dict.key
		context.Userdetails=frappe.db.get_list('User', fields=["username","first_name","full_name","email","last_name","username","gender","mobile_no","birth_date","location","reset_password_key"], filters={'reset_password_key':Key})
		Data=Userdetails[0].email
		context.Userdetails=Userdetails
		context.Rdata=frappe.db.get_list('Member', fields=["name","member_name","membership_type","email","gender","active","last_name","membership_expiry_date","phone_no","date_of_birth"], filters={'email':Data})
		context.show_sidebar=False
		context.no_breadcrumbs = True
		context.parents = [{"name":"me", "title":_("My Account")}]

