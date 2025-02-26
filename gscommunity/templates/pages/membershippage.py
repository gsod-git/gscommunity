# -*- coding: utf-8 -*-
# Copyright (c) 2018, valiantsystems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils import getdate, add_months, add_to_date
from frappe.website.utils import clear_cache
from frappe.utils import getdate
from datetime import date
from frappe.utils.oauth import get_oauth2_authorize_url, get_oauth_keys, login_via_oauth2, login_oauth_user as _login_oauth_user, redirect_post_login
import json
from frappe import _
from frappe.integrations.doctype.ldap_settings.ldap_settings import get_ldap_settings

no_cache = True

def get_context(context):
	if frappe.session.user != "Guest" and frappe.session.data.user_type=="System User":
		frappe.local.flags.redirect_location = "/desk"
		raise frappe.Redirect

	# get settings from site config
	context.no_header = True
	context.for_test = 'login.html'
	context["title"] = "Membership"
	context["disable_signup"] = frappe.utils.cint(frappe.db.get_value("Website Settings", "Website Settings", "disable_signup"))

	# for provider in ("google", "github", "facebook", "frappe"):
	# 	if get_oauth_keys(provider):
	# 		context["{provider}_login".format(provider=provider)] = get_oauth2_authorize_url(provider)
	# 		context["social_login"] = True

	ldap_settings = get_ldap_settings()
	context["ldap_settings"] = ldap_settings

	login_name_placeholder = [_("Email address")]

	if frappe.utils.cint(frappe.get_system_settings("allow_login_using_mobile_number")):
		login_name_placeholder.append(_("Mobile number"))

	if frappe.utils.cint(frappe.get_system_settings("allow_login_using_user_name")):
		login_name_placeholder.append(_("Username"))

	context['login_name_placeholder'] = ' {0} '.format(_('or')).join(login_name_placeholder)

	return context

@frappe.whitelist()
def validate_members(first_name, email, mobile_no):
	member=frappe.db.get_all('User', fields=['first_name','email','mobile_no'], filters={'first_name':first_name,'email':email,'mobile_no':mobile_no})
	if member:
		for item in member:
			memberdetails= frappe.db.get_all('Member', fields=['name','member_name','membership_type','email','gender','last_name','phone_no','date_of_birth','address_line_1','city','zip_code','address_line_2','state','newsletter'], filters={'email':item.email}, limit_page_length=1)
			return memberdetails
    # else:
    	# memberdetails= frappe.db.get_all('Member', fields=['member_name','membership_type','email','gender','last_name','phone_no','date_of_birth','address_line_1','city','zip_code','address_line_2','state','newsletter'], filters={'email':item.email})
    	# return member