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
# from frappe.integrations.doctype.ldap_settings.ldap_settings import get_ldap_settings
from frappe.utils.password import get_decrypted_password
from frappe.integrations.doctype.ldap_settings.ldap_settings import LDAPSettings

no_sitemap = 1
no_cache = 1

def get_context(context):
	Data= ''
	ldap_settings = LDAPSettings.get_ldap_client_settings()
	frappe.log_error("@@__context__",context)
	context["ldap_settings"] = ldap_settings
	if frappe.session.user!='Guest' and frappe.session.user=='Administrator':
		context.Userdetails=frappe.db.get_all('User', fields=["username","first_name","full_name","email","last_name","username","gender","mobile_no","birth_date","location"], filters={'username':frappe.session.user})
		Data=context.Userdetails[0].email
		context.Userdetails=context.Userdetails
		context.Rdata=frappe.db.get_all('Member', fields=["name","member_name","membership_type","email","gender","active","last_name","membership_expiry_date","phone_no","date_of_birth"], filters={'email':Data})
		context.YellowpagesList=frappe.db.get_all('Yellow Pages', fields=['business_name','route','business_type','category','subcategory','owner_name','email','address','phone','image','description'], filters={'owner':frappe.session.user})
		context.show_sidebar=True
		context.no_breadcrumbs = True
		context.parents = [{"name":"me", "title":_("My Account")}]
	if frappe.session.user!='Guest' and frappe.session.user!='Administrator':
		Userdetails=frappe.db.get_all('User', fields=["first_name","full_name","email","last_name","username","gender","mobile_no","birth_date","location"], filters={'email':frappe.session.user})
		Data=Userdetails[0].email
		context.Userdetails=Userdetails
		context.Rdata=frappe.db.get_all('Member', fields=["name","member_name","membership_type","email","gender","active","last_name","membership_expiry_date","phone_no","date_of_birth"], filters={'email':Data})
		context.YellowpagesList=frappe.db.get_all('Yellow Pages', fields=['business_name','route','business_type','category','subcategory','owner_name','email','address','phone','image','description'], filters={'owner':frappe.session.user})
		context.show_sidebar=True
		context.no_breadcrumbs = True
		context.parents = [{"name":"me", "title":_("My Account")}]
	if frappe.session.user=='Guest':
		Key=frappe.form_dict.key
		frappe.log_error("@@__Key__",Key)
		context.Userdetails=frappe.db.get_all('User', fields=["username","first_name","full_name","email","last_name","username","gender","mobile_no","birth_date","location","reset_password_key"], filters={'reset_password_key':Key})
		frappe.log_error("@@__context.Userdetails__",context.Userdetails)
		if context.Userdetails:
			if context.Userdetails[0]:
				Data=context.Userdetails[0].email
				# context.Userdetails=context.Userdetails
		context.Rdata=frappe.db.get_all('Member', fields=["name","member_name","membership_type","email","gender","active","last_name","membership_expiry_date","phone_no","date_of_birth"], filters={'email':Data})
		context.show_sidebar=False
		context.no_breadcrumbs = True
		context.parents = [{"name":"me", "title":_("My Account")}]
