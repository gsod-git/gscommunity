# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
# import frappe
# from _future_ import unicode_literals
import frappe
import frappe.utils
from frappe.utils.oauth import get_oauth2_authorize_url, get_oauth_keys, login_via_oauth2, login_via_oauth2_id_token, login_oauth_user as _login_oauth_user, redirect_post_login
import json
from frappe import _
from frappe.auth import LoginManager
from frappe.integrations.doctype.ldap_settings.ldap_settings import get_ldap_settings
from frappe.utils.password import get_decrypted_password
from frappe.utils.html_utils import get_icon_html

def get_context(context):
	EventsList=frappe.db.get_all('Events',fields=['name','published','route','location','start_date','end_date','banner_image'], filters={'published':1}, order_by='start_date desc', limit_page_length=3)
	context.Events=EventsList
	# SponsorsList=frappe.db.get_all('Sponsorship Type',fields=['name'])
	# print(EventsList)	
	# for item in SponsorsList:
	# 	item.Sponsors=frappe.db.get_all('Sponsors',fields=['company_name','starts_on','expires_on','logo','description'],filters={'parent':self.name})
	# MembershipType=frappe.db.get_all('Membership Type',fields=['membership_type','amount'])
	# context.EventsList=EventsList
	# context.SponsorsList=SponsorsList
	# context.MembershipType=MembershipType
	# HomeSliders = frappe.db.get_all('HomeSliders', fields=['slidername','sub_title','sliderurl','imageurl','displayorder'],order_by='displayorder',limit_page_length=10)	
	# context.Sliders=HomeSliders
	# 
	